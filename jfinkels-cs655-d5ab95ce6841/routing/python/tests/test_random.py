# test_random.py - unit tests for the random module
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `random` module."""
import unittest

from routing.random import OSIRandom

__all__ = ['OSIRandomTest']
"""The names of all the test cases, so that when other modules do `import *
from test_random`, they get the names of all the test cases.

"""


class OSIRandomTest(unittest.TestCase):
    """Tests for the `OSIRandom` class.

    These tests are designed to ensure that the seed and pseudo-random numbers
    generated by this class match those of the implementation provided in the
    Java source code for this assignment.

    """

    def setUp(self):
        """Initializes the pseudo-random number generator with a fixed seed."""
        self.r = OSIRandom(1234)

    def test___init__(self):
        """Tests that the seed is correctly initialized."""
        self.assertEqual(1234, self.r.seed)

    def test_next_double(self):
        """Tests that generating a random floating point number produces the
        same results as in the original Java implementation.

        """
        x = self.r.next_double()
        y = self.r.next_double()
        z = self.r.next_double()
        self.assertEqual((0.108584856715598, 0.0598162785729545,
                          0.03988769188512833), (x, y, z))

    def test_next_int(self):
        """Tests that generating a random integer produces the same results as
        in the original Java implementation.

        """
        x = self.r.next_int()
        y = self.r.next_int()
        z = self.r.next_int()
        self.assertEqual((3558, 1960, 1307), (x, y, z))
