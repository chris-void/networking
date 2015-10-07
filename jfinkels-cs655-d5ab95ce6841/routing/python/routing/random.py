# random.py - an implementation of a pseudo-random number generator
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides a pseudo-random number generator for the simulation."""

import random


class OSIRandom(object):
    """A pseudo-random number generator."""

    def __init__(self, seed=None):
        """Initializes this pseudo-random number generator with the specified
        seed integer.

        If `seed` is `None`, a random integer in the interval [0, 32768) will
        be used.

        """
        if seed is None:
            seed = random.randrange(0xFFFFFFFF)
        self.seed = seed & 0xFFFFFFFF

    def next_double(self):
        """Returns a random floating point number between 0 and 1."""
        return self.next_int() / 32767.0

    def next_int(self):
        """Returns a random integer between 0 and 32768."""
        self.seed = ((self.seed & 0xFFFFFFFF) * (1103515245 & 0xFFFFFFFF)
                     + 12345) & 0xFFFFFFFF
        return (self.seed // 65536) % 32768


_instance = OSIRandom()
"""The singleton instance of the random number generator."""

initialize = _instance.__init__
next_double = _instance.next_double
