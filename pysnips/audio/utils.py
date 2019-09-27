"""
Helper functions to solve common problems/tasks when
messing with audio files
"""

import numpy as np
import soundfile as sf
import itertools
from collections import OrderedDict

__all__ = ['ambisonics_reorder_channels',
           'extract_channels_from_wav',
           'monofiles_to_multitrack']


FUMA = OrderedDict(enumerate(['w',
                              'x', 'y', 'z',
                              'r', 's', 't', 'u', 'v',
                              'k', 'l', 'm', 'n', 'o', 'p', 'q']))
ACN = OrderedDict(enumerate(['w',
                             'y', 'z', 'x',
                             'v', 't', 'r', 's', 'u',
                            'q', 'o', 'm', 'k', 'l', 'n', 'p']))
AMBISONICS_ORDERINGS = {'fuma': FUMA, 'acn': ACN}


def _ambisonics_channel_count_from_order(order, three_dim=True):
    """
    Helper function that computes the number of channels for a given ambisonics order.
    """
    return (order + 1)**2 if three_dim else (2 * order + 1)


def ambisonics_reorder_channels(signal_array, order, input_ordering, output_ordering):
    """
    Reorder ambisonics signals from one channel ordering to another.

    signal_array - Array with the signals as given by soundfile.read from a wav file
    order - order of the ambisonics signals, full sphere representation is assumed
    input_ordering - name of channel ordering of the array ['fuma', 'acn']
    output_ordering - desired output ordering ['fuma', 'acn']
    """
    channel_count = _ambisonics_channel_count_from_order(order)
    assert(signal_array.shape[1] == channel_count)
    input_ordering = OrderedDict(itertools.islice(AMBISONICS_ORDERINGS[input_ordering].items(), channel_count))
    output_ordering = OrderedDict(itertools.islice(AMBISONICS_ORDERINGS[output_ordering].items(), channel_count))
    input_ordering = {v: k for k, v in input_ordering.items()}
    new_order = [input_ordering[output_ordering[i]] for i in output_ordering.keys()]

    return signal_array[:, new_order]


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
