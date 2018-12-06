# -*- coding: utf-8 -*-

"""
Radar chart plotting

Most of the code is taken from:
    https://matplotlib.org/examples/api/radar_chart.html
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection

FULL_CIRCLE_DEG = 360

def plot_radar_chart(data, line_labels, var_labels, **kwargs):
    """Make a radar chart.

    Input data is assumed to differ in variables along the columns and differ in
    observations/samples along the rows.

    Parameters
    ----------
    data: sequence, one- or two-dimensional
        Data to plot. Must be some sort of sequence that can be converted to a numpy array
    line_labels: sequence, one-dimensional
        Labels for the legend of the plot
    var_labels: sequence, one-dimensional
        Labels for the 'theta-axes'
    kwargs: keyword arguments
        can be either:
            `title` - string, title for the figure
            `r_ticks` - sequence, positions for the radial ticks
            `r_tick_labels` - sequence, labels for the radial ticks given by `r_ticks`
            `colours` - sequence with matplotlib colours for the lines
        or keyword args accepted by create_radar_chart function
    """
    # get kwargs that should not be passed on to create_radar_chart
    title = kwargs.pop('title', '')
    r_ticks = kwargs.pop('r_ticks', None)
    r_tick_labels = kwargs.pop('r_tick_labels', None)
    colours = kwargs.pop('colours', None)

    # validate input data
    data, d_rows, d_cols = _handle_input_data(data)

    # plot the thing
    theta = _theta(d_cols)
    fig, ax = create_radar_chart(d_cols, **kwargs)
    for i in range(d_rows):
        if colours is None:
            ax.plot(theta, data[i], label=line_labels[i])
        else:
            ax.plot(theta, data[i], label=line_labels[i], color=colours[i])
    if r_ticks is not None:
        ax.set_yticks(r_ticks)
    if r_tick_labels is not None:
        ax.set_yticklabels(r_tick_labels)
    ax.set_rscale(np.max(data), round_up=True)
    ax.set_varlabels(var_labels)
    ax.legend()
    fig.suptitle(title)
    plt.show()

    return fig, ax


def _handle_input_data(data):
    """Helper function for input data validation and calculating helper values"""
    data = np.asarray(data)
    if np.ndim(data) == 1:
        d_rows = 1
        d_cols = len(data)
        data = data.reshape((1, data.shape[0]))
    elif np.ndim(data) == 2:
        d_rows = data.shape[0]
        d_cols = data.shape[1]
    else:
        raise ValueError("Incorrect dimensionality of data. Must be <= 2")
    return data, d_rows, d_cols


def _unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def _theta(num_vars):
    """Return array of theta values.
    Values are evenly spaced and corrected for radar plotting
    """
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2
    return theta


def create_radar_chart(num_vars, frame='polygon', **kwargs):
    """Create a radar chart with `num_vars` axes.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.
    kwargs: keyword arguments for `matplotlib.pyplot.subplots`
        most likely: nrows, ncols
        for others see: https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.subplots.html

    """
    theta = _theta(num_vars)

    def draw_poly_patch(self):
        verts = _unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):
        """
        Projection class for a radar chart
        """

        name = 'radar'
        size = num_vars
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        shape = frame
        draw_patch = patch_dict[frame]

        def set_rscale(self, top, bottom=0, round_up=False):
            """Scale the radar chart
                If circle chart then this function just sets the ylim of the polar ax.
                If polygon chart then ylim will be set to fit a circle with radius h
                completely inside it (distance from center to midpoint of polygon 
                edge will be h.
            """
            if self.shape == 'circle':
                r = top
            elif self.shape == 'polygon':
                angle_of_slice = 2 * np.pi / self.size
                r = top / np.cos(angle_of_slice / 2.)
                if round_up:
                    r = np.ceil(r)
            else:
                # this should never happen since this is checked for in class
                # creation
                raise ValueError('unknown value for `frame`: %s' % self.shape)
            self.set_ylim(bottom, r)

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            """Label the radial axes"""
            self.set_thetagrids(np.degrees(theta) % FULL_CIRCLE_DEG, labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = _unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    
    # if subplot_kw argument is given, overwrite projection field
    # TODO: maybe throw error when projection is given?
    if 'subplot_kw' in kwargs:
        kwargs['subplot_kw']['projection'] = 'radar'
    else:
        kwargs['subplot_kw'] = {'projection': 'radar'}
    fig, axes = plt.subplots(**kwargs)

    return fig, axes
