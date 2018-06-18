"""
Helper functions to solve common problems/tasks when 
messing with audio files
"""

import numpy as np
import soundfile as sf


def extract_channels_from_wav(filename, channels, write_file=None):
    """Read wav file and extract only the specified channel numbers"""
    s, fs = sf.read(filename)
    if type(channels) == int:
        channels = [channels]
    s = s[:,channels]
    if write_file is not None:
        sf.write(write_file, s, fs)
    return s