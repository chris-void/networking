# helpers.py - supporting base classes for test cases
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides base classes for test cases."""
import sched
import unittest

from routing.random import OSIRandom
from routing.datacontainers import Packet

SEED = 3322
"""The seed for the pseudo-random number generator for the tests in this
module.

"""


class TestSupport(unittest.TestCase):
    """Base class for all test classes in this module which maintains the
    scheduler and the time functions.

    """

    def setUp(self):
        """Creates the scheduler, initializes the scheduler time to 0, and
        initializes a pseudo-random number generator.

        """
        self.time = 0
        self.scheduler = sched.scheduler(self.get_time, self.delay)
        self.random = OSIRandom(SEED)
        self.addTypeEqualityFunc(Packet, self.assertPacketEqual)

    def clear_queue(self):
        """Clears the event queue for the scheduler (using black magic!)."""
        for event in list(self.scheduler.queue):
            self.scheduler.cancel(event)

    def get_events(self):
        """Returns the ordered list of events currently in the scheduler's
        queue.

        """
        return list(self.scheduler.queue)

    def assertPacketEqual(self, packet1, packet2, msg=None):
        """Asserts that the two `Packet` objects have equal state."""
        self.assertEqual(packet1.source, packet2.source, msg)
        self.assertEqual(packet1.dest, packet2.dest, msg)
        self.assertEqual(packet1.mincosts, packet2.mincosts, msg)

    def delay(self, delay_amount):
        """Delays the current simulation by the specified delay."""
        self.time += delay_amount

    def get_time(self):
        """Returns the current simulation time."""
        return self.time
