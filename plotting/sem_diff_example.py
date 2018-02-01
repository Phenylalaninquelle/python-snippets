#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example usage of plot_sem_diff function
"""

import numpy as np
from semantic_differential import plot_sem_diff

def main():
    # randomly sampled data
    data = np.random.randint(1,5, (4,5))
    #data[2,3] = np.nan
    # the differentials in our fake data
    # here we want labels on both sides of the plot (like a proper differential)
    left = ['small', 'quiet', 'weak', 'dark', 'bad']
    right = ['big', 'loud', 'strong', 'bright', 'good']
    # careful: the conversion to list is necessary since zip objects
    # wont get properly converted to numpy arrays
    y_labels = list(zip(left, right))
    title = 'This is the title'
    # labels of the different lines for the legend
    observations = ['A', 'B', 'C', 'D']
    # our data has values from 1 to 4 so we set the appropriate labels and an offset
    x_labels = np.arange(1,5)
    x_offset = 1

    # only small padding left and right of the lines
    x_pad = 0.1

    fig = plot_sem_diff(data, x_labels, y_labels, x_pad=x_pad, x_offset=x_offset,
                        line_labels=observations, title=title)

    # make another plot with identical data for each observation to show jittering
    data2 = 3 * np.ones((4,5))
    data2[:, 0] = np.asarray([1,2,3,4])
    fig = plot_sem_diff(data2, x_labels, y_labels, x_pad=x_pad, x_offset=x_offset,
                        line_labels=observations, title=title, jitter_amount=.01)

if __name__ == '__main__':
    main()
