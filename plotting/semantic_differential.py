"""
Create a profile plot aka semantic differential
"""

import matplotlib.pyplot as plt
from numpy import where, isnan, split, arange, asarray
from pandas import DataFrame

def plot_sem_diff(df, x_labels, y_labels, colours, labels, title=''):
    #TODO: make labels optional or something
    """
    Plot the semantic differential of the values given by `df`

    TODO: df should accept any seuence type
    df - pandas DataFrame with the data
    x_labels - labels for the values on the x axis
    y_labels - sequence of labels for the y axes
        If given a one-dimensional sequence (i.e. a seq of labels), labels will 
        only appear at the right of the figure. If given a sequence of pairs, then
        both sides will be labeled with the paired labels facing each other
    colours - sequence of colours to use when plotting the rows of the DataFrame
    labels - sequence of strings to use as labels for the lines
    title - title for the figure
    """
    # error checking
    if type(df) != DataFrame:
        raise ValueError("Must pass DataFrame!!")
    L = len(df)
    if L != len(colours):
        raise ValueError("There must be a colour for every row in the DataFrame!")

    left_labels, right_labels = __get_labels(y_labels) 

    fig = plt.figure()
    y = arange(len(df.columns))[::-1]

    for i in range(L):
        __do_plot(df.loc[i], y, colour=colours[i], label=labels[i])

    plt.title(title)
    #TODO: this only works for the x labels being numbers
    plt.xticks(x_labels, x_labels)
    plt.xlim(x_labels[0] - 0.2, x_labels[-1] + 0.2)
    if left_labels is None:
        plt.tick_params(labelleft=False, labelright=True)
        plt.yticks(y, right_labels)
    else:
        ax_l = fig.gca()
        plt.yticks(y, left_labels)
        ax_r = ax_l.twinx()
        ax_r.set_ylim(ax_l.get_ylim())
        plt.yticks(y, right_labels)
        plt.sca(ax_l)
    plt.grid()
    #TODO: adjustment needed, when labels become optional one day
    plt.legend()
    plt.tight_layout()

def __do_plot(data, y, colour, label):
    """
    Wrapper for the actual plotting that takes care of missing values in the data
    (represented by `Nan`).

    data - x-axis data
    y - y-axis data
    colour - colour for the plot
    label - label for the line
    """
    data = asarray(data)
    y = asarray(y)
    if len(data.shape) !=1 and data.shape[1] > 1:
        raise ValueError("__do_plot handles only one-d data!")

    x, y = __split_by_nan(data, y)

    for x_arr, y_arr in zip(x, y):
        plt.plot(x_arr, y_arr, color=colour, linestyle='--', marker='x', label=label)

def __get_labels(y_labels):
    """
    Handle the given y-axis labels.
    """
    y_labels = asarray(y_labels)
    dim = y_labels.ndim
    if dim == 1:
        if len(y_labels) == 0:
            raise ValueError("Can't pass empty array of y-axis labels")
        right_labels = y_labels
        left_labels = None
    if dim > 2:
        raise ValueError("Can only pass one- or twodimensional arrays of y-axis labels")
    if dim == 2:
        shape = y_labels.shape
        # this check serves the purpose of ensuring that the labels are given by a
        # sequence of pairs (which makes shape[1] = 2), one could use len(y) to
        # find the axis with the labels and infer the array's shape but if only two
        # labels are given this results in ambiguity (maybe there is another smart
        # way but for now the arguments has to be in shape (N,2)
        if shape[1] != 2:
            raise ValueError("y_labels given in incorrect shape")
        left_labels = y_labels.T[0]
        right_labels = y_labels.T[1]
    return left_labels, right_labels


def __split_by_nan(x, y):
    """
    Split `x` up into subsequences seperated by Nan values. If no Nan values are
    present in `x` then only one subsequence is generated (being `x`). Split up
    `y` in equal shapes as `x`.

    Returns two sequences. The first contains the subsequences of `x`, the second
    those of `y`.
    """
    nan_pos = where(isnan(x))[0]
    if len(nan_pos) == 0:
        return [x], [y]
   
    # split the arrays by nan values in it and then collects the subarrays
    # in a list without the nan value or the corresponding y value respectively
    x_ret = [a if i==0 else a[1:] for i, a in enumerate(split(x, nan_pos))]
    y_ret = [a if i==0 else a[1:] for i, a in enumerate(split(y, nan_pos))]
    return x_ret, y_ret
