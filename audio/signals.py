"""
Module for generating commonly used signals for testing or stuff.
"""

import numpy as np


def white_noise(length_seconds, fs, amp, db=True):
    """
    Generate white noise signal

    length_seconds: length of the signal in seconds
    fs: sampling frequency
    amp: maximum amplitude (next argument specifies db or lin)
    db: if true, amp is interpreted as decibels, otherwise as linear factor
    """
    amp = 10 ** (amp / 20) if db else amp
    return (np.random.rand(length_seconds * fs) - 0.5) * amp * 2
