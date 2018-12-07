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
    s = s[:, channels]
    if write_file is not None:
        sf.write(write_file, s, fs)
    return s


def monofiles_to_multitrack(monofiles, new_filename):
    """Read mono wav files and combine them into a multitrack wavfile"""
    # TODO: this causes MemoryError when signals are very long
    signals = []
    for f in monofiles:
        s, fs = sf.read(f)
        signals.append(s)
    multitrack_array = np.asarray(signals).T
    sf.write(new_filename, multitrack_array, fs)
