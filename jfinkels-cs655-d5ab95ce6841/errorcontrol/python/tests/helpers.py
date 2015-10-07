# helpers.py - supporting base classes for test cases
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides base classes for test cases, including `TestSupport` and
`LinkedTestSupport` (for classes which require sending data along a link to an
endpoint).

"""
import sched
import unittest

from simulation.random import OSIRandom
from simulation.datacontainers import Packet
from simulation.endpoints.bases import Endpoint
from simulation.links import UnidirectionalLink

SEED = 1234
"""The seed for the pseudo-random number generator for the tests in this module.

"""


class TestSupport(unittest.TestCase):
    """Base class for all test classes in this module which maintains the
    scheduler and the time functions.

    """

    def setUp(self):
        """Creates the scheduler, initializes the scheduler time to 0, and
        initializes a pseudo-random number generator.

        """
        self.scheduler = sched.scheduler(self.get_time, self.delay)
        self.time = 0
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
        self.assertEqual(packet1.data, packet2.data, msg)
        self.assertEqual(packet1.seqnum, packet2.seqnum, msg)
        self.assertEqual(packet1.acknum, packet2.acknum, msg)
        self.assertEqual(packet1.checksum, packet2.checksum, msg)

    def assertPacketNotEqual(self, packet1, packet2, msg=None):
        """Asserts that the two `Packet` objects do not have equal state."""
        p1 = (packet1.data, packet1.seqnum, packet1.acknum, packet1.checksum)
        p2 = (packet2.data, packet2.seqnum, packet2.acknum, packet2.checksum)
        self.assertNotEqual(p1, p2)

    def delay(self, delay_amount):
        """Delays the current simulation by the specified delay."""
        self.time += delay_amount

    def get_time(self):
        """Returns the current simulation time."""
        return self.time


class LinkedTestSupport(TestSupport):
    """A base class for tests that involve sending messages by way of a link."""

    def setUp(self):
        """Initializes a link with a destination endpoint for it."""
        super().setUp()
        self.destination = Endpoint(self.scheduler)
        self.link = UnidirectionalLink(self.scheduler, self.destination,
                                       self.random)
