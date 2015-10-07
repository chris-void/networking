# random.py - an implementation of a pseudo-random number generator
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides a pseudo-random number generator for the simulation."""

import random


class OSIRandom(object):
    """A pseudo-random number generator."""

    def __init__(self, seed=None):
        """Initializes this pseudo-random number generator with the specified
        seed integer.

        """
        if seed is None:
            seed = random.randrange(0xFFFFFFFF)
        self.seed = [(seed + i) & 0xFFFFFFFF for i in range(5)]

    def next_double(self, i):
        """Returns a random floating point number between 0 and 1, using the
        specified integer `i` as an intermediate seed.

        """
        return self.next_int(i) / 32767.0

    def next_int(self, i):
        """Returns a random integer between 0 and 32768, using the specified
        integer `i` as an intermediate seed.

        """
        self.seed[i] = ((self.seed[i] & 0xFFFFFFFF)
                        * (1103515245 & 0xFFFFFFFF) + 12345) & 0xFFFFFFFF
        return int(self.seed[i] / 65536) % 32768
