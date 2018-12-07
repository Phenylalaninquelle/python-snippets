import itertools
from collections import OrderedDict


FUMA = OrderedDict(enumerate(['w',
                              'x', 'y', 'z',
                              'r', 's', 't', 'u', 'v',
                              'k', 'l', 'm', 'n', 'o', 'p', 'q']))
ACN = OrderedDict(enumerate(['w',
                             'y', 'z', 'x',
                             'v', 't', 'r', 's', 'u',
                            'q', 'o', 'm', 'k', 'l', 'n', 'p']))
ORDERINGS = {'fuma': FUMA, 'acn': ACN}


def _channel_count_from_order(order, three_dim=True):
    """
    Helper function that computes the number of channels for a given ambisonics order.
    """
    return (order + 1)**2 if three_dim else (2 * order + 1)


def reorder_channels(signal_array, order, input_ordering, output_ordering):
    """
    Reorder ambisonics signals from one channel ordering to another.

    signal_array - Array with the signals as given by soundfile.read from a wav file
    order - order of the ambisonics signals, full sphere representation is assumed
    input_ordering - channel ordering of the array
    input_ordering - desired output ordering
    """
    channel_count = _channel_count_from_order(order)
    assert(signal_array.shape[1] == channel_count)
    input_ordering = OrderedDict(itertools.islice(ORDERINGS[input_ordering].items(), channel_count))
    output_ordering = OrderedDict(itertools.islice(ORDERINGS[output_ordering].items(), channel_count))
    input_ordering = {v: k for k, v in input_ordering.items()}
    new_order = [input_ordering[output_ordering[i]] for i in output_ordering.keys()]

    return signal_array[:, new_order]
