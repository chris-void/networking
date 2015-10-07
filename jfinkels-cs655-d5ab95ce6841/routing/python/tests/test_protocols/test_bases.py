# test_bases.py - unit tests for the routing.protocols.bases module
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `routing.protocols.bases` module."""
import io
import unittest

from routing.datacontainers import Packet
from routing.protocols.bases import Node

from ..helpers import TestSupport

__all__ = ['NodeTest']
"""The names of all the test cases, so that when other modules do `import *
from test_bases`, they get the names of all the test cases.

"""


class NodeTest(TestSupport):
    """Tests for the `Node` class."""

    def setUp(self):
        """Initializes the node to test.

        """
        super().setUp()
        self.node0 = Node(self.scheduler, 0, {0:0, 1:1}, 2)
        self.node1 = Node(self.scheduler, 1, {0:5, 1:4}, 2)
        nodes = {0: self.node0, 1: self.node1}
        self.node0.initialize(nodes)
        self.node1.initialize(nodes)
        # the call to initialize should schedule two initial arrival events
        self.assertEqual(2, len(self.get_events()))
        self.assertEqual(0, self.scheduler.timefunc())

    def test_last_arrival_time(self):
        """Test for getting the last arrival time."""
        self.scheduler.enterabs(10, 0, self.node0.from_layer2, ())
        self.scheduler.enterabs(20, 0, self.node0.from_layer2, ())
        self.scheduler.enterabs(30, 0, self.node1.from_layer2, ())
        self.scheduler.enterabs(40, 0, self.node0.from_layer2, ())
        self.assertEqual(30, self.node0.last_arrival_time(1))
        self.assertEqual(40, self.node1.last_arrival_time(0))

    def events_for_node1(self):
        """Returns a list of scheduled arrival events at node 1."""
        filter_func = lambda e: e.action == self.node1.from_layer2
        return list(filter(filter_func, self.scheduler.queue))

    def events_for_node0(self):
        """Returns a list of scheduled arrival events at node 0."""
        filter_func = lambda e: e.action == self.node0.from_layer2
        return list(filter(filter_func, self.scheduler.queue))

    def test_schedule_arrival(self):
        """Tests that a packet arrival event is correctly scheduled."""
        packet = Packet(0, 1, 'foo')
        self.node0.schedule_arrival(packet)
        events_for_node1 = self.events_for_node1()
        self.assertEqual(2, len(events_for_node1))
        event = max(events_for_node1)
        self.assertGreater(event.time, 0)
        self.assertEqual(self.node1.from_layer2, event.action)
        self.assertEqual(packet, event.argument[0])

        self.node0.schedule_arrival(packet)
        events_for_node1 = self.events_for_node1()
        self.assertEqual(3, len(events_for_node1))
        event2 = max(events_for_node1)
        self.assertGreater(event2.time, event.time)

    def test_to_layer2(self):
        """Tests that a packet sent to layer 2 has a corresponding packet
        arrival correctly scheduled on the destination node.

        """
        packet = Packet(0, 1, 'foo')
        self.node0.to_layer2(packet)
        self.assertEqual(3, len(self.get_events()))
        event = self.get_events()[-1]
        self.assertGreater(event.time, 0)
        self.assertEqual(self.node1.from_layer2, event.action)
        self.assertEqual(packet, event.argument[0])

        self.node0.to_layer2(packet)
        self.assertEqual(4, len(self.get_events()))
        event2 = self.get_events()[-1]
        self.assertGreater(event2.time, event.time)

    @unittest.skip
    def test_pretty_print(self):
        self.fail('Not yet implemented.')

    @unittest.skip
    def test___str__(self):
        self.fail('Not yet implemented.')
