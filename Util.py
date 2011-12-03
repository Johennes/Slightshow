##############################################################################
## Util.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

from itertools import cycle, islice

def roundrobin(*iterables):
    """Generator function, that recursively iterates over the items of a
    collection, e.g. roundrobin('ABC', 'D', 'EF') --> A D E B F C. Based on
    the Python recipe by George Sakkis."""
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))
