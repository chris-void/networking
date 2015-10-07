# test_distancevector.py - unit tests for routing.protocols.distancevector
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `routing.protocols.distancevector` module."""
from routing.datacontainers import Packet
from routing.protocols.bases import INFINITY
from routing.protocols.distancevector import DistanceVectorNode

from ..helpers import TestSupport

__all__ = ['DistanceVectorNodeTest']
"""The names of all the test cases, so that when other modules do `import *
from test_distancevector`, they get the names of all the test cases.

"""


class DistanceVectorNodeTest(TestSupport):
    """Tests for the `DistanceVectorNode` class."""

    def setUp(self):
        """Initializes the node to test."""
        super().setUp()
        self.node0 = DistanceVectorNode(self.scheduler, 0, {0:0, 1:1, 2:INFINITY}, 3)
        self.node1 = DistanceVectorNode(self.scheduler, 1, {0:1, 1:0, 2:1}, 3)
        self.node2 = DistanceVectorNode(self.scheduler, 2, {0:INFINITY, 1:1, 2:0}, 3)
        nodes = dict(enumerate((self.node0, self.node1, self.node2)))
        self.node0.initialize(nodes)
        self.node1.initialize(nodes)
        self.node2.initialize(nodes)

    def test_from_layer2(self):
        self.fail('Not yet implemented.')

    def test_link_changed(self):
        self.fail('Not yet implemented.')
