# test_links.py - unit tests for the links module
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `links` module."""
from simulation.datacontainers import Packet
from simulation.endpoints.bases import Endpoint
from simulation.links import UnidirectionalLink
from simulation.links import UnreliableUnidirectionalLink

from .helpers import LinkedTestSupport
from .helpers import TestSupport

__all__ = ['UnidirectionalLinkTest', 'UnreliableUnidirectionalLinkTest']
"""The names of all the test cases, so that when other modules do `import *
from test_links`, they get the names of all the test cases.

"""


class UnidirectionalLinkTest(LinkedTestSupport):
    """Tests for the `UnidirectionalLink` class."""

    def test_send(self):
        """Tests that packets send along the link arrive at the destination.

        """
        self.fail('Not yet implemented.')


class UnreliableUnidirectionalLinkTest(TestSupport):
    """Tests for the `UnreliableUnidirectionalLink` class."""

    def setUp(self):
        """Initializes the destination endpoint for the link to be tested."""
        super().setUp()
        self.destination = Endpoint(self.scheduler)

    def test_send_no_error_no_congestion(self):
        """Tests that sending a packet on an unreliable link with no error
        probability and no congestion on the receiving end will cause the sent
        packet to arrive unharmed.

        """
        link = UnreliableUnidirectionalLink(self.scheduler, self.destination, 0,
                                            0, self.random)
        packet = Packet(0, 0, 0, 'foo')
        link.send(packet)
        events = self.get_events()
        self.assertEqual(1, len(events))
        event = events[0]
        self.assertGreater(event.time, self.scheduler.timefunc())
        self.assertEqual(self.destination._from_layer3, event.action)
        self.assertEqual(1, len(event.argument))
        self.assertEqual(packet, event.argument[0])

    def test_send_no_error_congestion(self):
        """Tests that sending a packet on an unreliable link with congestion
        on the receiving end will cause its arrival time to be after the last
        arrival time of the packets already scheduled for arrival.

        """
        link = UnreliableUnidirectionalLink(self.scheduler, self.destination, 0,
                                            0, self.random)
        packet1 = Packet(0, 0, 0, 'foo')
        packet2 = Packet(1, 0, 0, 'foo')
        packet3 = Packet(2, 0, 0, 'foo')
        link.send(packet1)
        link.send(packet2)
        link.send(packet3)
        events = self.get_events()
        self.assertEqual(3, len(events))
        event1, event2, event3 = events
        self.assertLess(event1.time, event2.time)
        self.assertLess(event2.time, event3.time)

    def test_send_loss_probability(self):
        """Tests that sending a packet on an unreliable link with a loss
        probability of 1 ensures that the packet never arrives.

        """
        link = UnreliableUnidirectionalLink(self.scheduler, self.destination, 1,
                                            0, self.random)
        packet1 = Packet(0, 0, 0, 'foo')
        packet2 = Packet(1, 0, 0, 'foo')
        packet3 = Packet(2, 0, 0, 'foo')
        link.send(packet1)
        link.send(packet2)
        link.send(packet3)
        events = self.get_events()
        self.assertEqual(0, len(events))

    def test_send_corruption_probability(self):
        """Tests that sending a packet on an unreliable link with a corruption
        probability of 1 ensures that the packet always arrives corrupted.

        """
        link = UnreliableUnidirectionalLink(self.scheduler, self.destination, 0,
                                            1, self.random)
        packet = Packet(0, 0, 0, 'foo')
        link.send(packet)
        event = self.get_events()[0]
        self.assertPacketNotEqual(packet, event.argument[0])
        packet = Packet(1, 0, 0, 'foo')
        link.send(packet)
        event = self.get_events()[0]
        self.assertPacketNotEqual(packet, event.argument[0])
