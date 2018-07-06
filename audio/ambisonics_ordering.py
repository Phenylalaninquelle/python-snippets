import itertools
from collections import OrderedDict


fuma = OrderedDict(enumerate(['w', 
                              'x', 'y', 'z', 
                              'r', 's', 't', 'u', 'v', 
                              'k', 'l', 'm', 'n', 'o', 'p', 'q']))
acn = OrderedDict(enumerate(['w',
                             'y', 'z', 'x',
                             'v', 't', 'r', 's', 'u',
                            'q', 'o', 'm', 'k', 'l', 'n', 'p']))
orderings = {'fuma': fuma, 'acn': acn}

def _channel_count_from_order(order, three_dim=True):
    c = (order + 1)**2 if three_dim else (2 * l + 1)
    return c

def reorder_channels(signal_array, order, input_order, output_order):
    """
    Reorder ambisonics signals from one channel ordering to another.

    signal_array - Array with the signals as given by soundfile.read from a wav file
    order - order of the ambisonics signals, full sphere representation is assumed
    from - channel ordering of the array
    to - desired output ordering
    """
    channel_count = _channel_count_from_order(order)
    assert(signal_array.shape[1] == channel_count)
    input_order = dict(itertools.islice(orderings[input_order].items(), channel_count))
    output_order = dict(itertools.islice(orderings[output_order].items(), channel_count))
    output_order = {v: k for k, v in output_order.items()}
    new_order = [output_order[input_order[i]] for i in input_order.keys()]
    print(new_order)

    return signal_array[:, new_order]