#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example usage of plot_radar_chart function
"""

import numpy as np
from radar_chart import plot_radar_chart

def main():
    # random sampled data
    data = np.random.randint(1,5, (4,5))
    # the variables in our fake data
    vars = ['Magnificance', 'Foolishness', 'Intelligence', 'Brilliance', 'Thrapp']
    title = 'This is the title'
    # labels of the different lines for the legend
    observations = ['A', 'B', 'C', 'D']
    # we want radial lines at 1,2,3,4 and 5 but only labels at 1,2,3 and 4
    r_ticks = [1,2,3,4,5]
    r_tick_labels = [1,2,3,4]

    fig, ax = plot_radar_chart(data, observations, vars, 
                               title=title, r_ticks=r_ticks,
                               r_tick_labels=r_tick_labels)

    # plot adjustments: if the theta labels overlap with the figure us this:
    # pad_length = 20
    # ax.tick_params(pad=pad_length)

if __name__ == '__main__':
    main()
