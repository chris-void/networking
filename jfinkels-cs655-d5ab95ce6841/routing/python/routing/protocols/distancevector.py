# distancevector.py - node which uses the distance vector routing protocol
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides the node class for the distance vector protocol.

Uses distributed Bellman-Ford with split horizon using poison reverse.

"""
import copy
import logging

from ..datacontainers import Packet
from .bases import INFINITY
from .bases import Node

STAR = None
"""Represents that there is no next node in a path."""

_logger = logging.getLogger(__name__)
"""The logger for this module."""


class Logger(object):
    """Wrapper for the `logging` module's normal logger which prepends the
    simulation time before logging the requested message.

    """

    def __init__(self, scheduler, logger):
        """Stores the scheduler, which maintains the simulation time, and the
        logger to use to log messages.

        """
        self.scheduler = scheduler
        self.logger = logger

    def debug(self, message):
        """Logs `message` with the current simulation time."""
        time = self.scheduler.timefunc()
        self.logger.debug('{:.3f}: {}'.format(time, message))

logger = None
"""This is the instance of the `Logger` class (defined in this module) which
wraps the Python built-in `logging` logger to provide the simulation time.

HACK: this is a global so we can keep existing code without changing calls to
`logger.debug`.

"""


class DistanceVectorNode(Node):
    """Uses a distance vector strategy implemented with the distributed
    Bellman-Ford algorithm (using split horizon with poison reverse) to
    determine the shortest path to other nodes in the graph.

    """

    def __init__(self, *args, **kw):
        """Initializes the routing table and distance matrix for this node."""
        super().__init__(*args, **kw)
        # HACK logger is global to allow wrapping logger.debug
        global logger
        logger = Logger(self.scheduler, _logger)
        self.routing_table = dict([(d, (STAR, INFINITY))
                                   for d in range(self.total_nodes)])
        self.d_i = self.link_costs
        self.D_i = [dict((n, INFINITY) for n in self.neighbors())
                    for m in range(self.total_nodes)]
        for k, d_ik in self.d_i.items():
            self.routing_table[k] = (k, d_ik)
        self.routing_table[self.node_id] = (STAR, 0)
        for n in self.neighbors():
            self.D_i[n][n] = self.d_i[n]

    def from_layer2(self, packet):
        """Updates the distance matrix with the new distances specified in the
        packet, updates the routing table if necessary due to changes in the
        distance matrix, and sends any changes to the neighbors of this node.

        """
        logger.debug('from_layer2(): {}'.format(packet))
        i, k, V_k = self.node_id, packet.source, packet.mincosts
        for (j, D_kj) in V_k:
            self.D_i[j][k] = D_kj + self.d_i[k]
        logger.debug('  distance matrix updated to:')
        self.log_distances()
        self.update_and_send()

    def initialize(self, all_nodes):
        """Stores `all_nodes` (a map from node ID to `Node` object for all
        nodes in the graph) and sends the initial packet to each of the other
        nodes.

        """
        self.nodes = all_nodes.copy()
        for neighbor in self.neighbors():
            V_i = [(dest, cost) for dest, cost in self.d_i.items()]
            packet = Packet(self.node_id, neighbor, V_i)
            self.to_layer2(packet)

    def link_down(self, link_id):
        """Updates the distance matrix and routing table due to a failure of
        the link between this node and the specified neighbor node ID.

        `link_id` is the ID of the neighbor whose link has failed.

        Pre-condition: the specified link was already up.

        """
        k = link_id
        for j in range(self.total_nodes):
            self.D_i[j][k] = INFINITY
        self.update_and_send()

    def link_up(self, link_id, new_cost):
        """Updates the distance matrix and routing table due to the link
        between this node and the neighbor with ID `link_id` becoming active
        with the specified new cost.

        Pre-condition: the specified link was already down.

        """
        logger.debug('link_up(): link {} cost {}'.format(link_id, new_cost))
        i, k = self.node_id, link_id
        d_ik = new_cost
        V_k = [(k, d_ik)]
        packet = Packet(k, i, V_k)
        self.from_layer2(packet)
        V_i = []
        for d in range(self.total_nodes):
            if d != self.node_id:
                V_i.append(self.routing_table[d])
        packet = Packet(i, k, V_i)
        logger.debug('link_up(): sending packet {}'.format(packet))
        self.to_layer2(packet)

    def link_changed(self, link_id, new_cost):
        """Called when the link between this node and the neighbor with ID
        `link_id` changes its cost to `new_cost`.

        Implementation: calls `link_down` followed immediately by `link_up`.

        """
        self.link_down(link_id)
        self.link_up(link_id, new_cost)

    def log_distances(self):
        """Logs the current distance matrix at the `DEBUG` level."""
        for dest, row in enumerate(self.D_i):
            logger.debug('  {}: {}'.format(dest, row))

    def log_routing_table(self):
        """Logs the current routing table at the `DEBUG` level."""
        for key, row in self.routing_table.items():
            logger.debug('  {}: {}'.format(key, row))

    def poison(self, packet):
        """Poisons `distance_vector` (*in-place*) with infinity at each index
        for which `neighbor` is the next hop to that destination.

        """
        for i in range(len(packet.mincosts)):
            destination = packet.mincosts[i][0]
            if self.routing_table[destination][0] == packet.dest:
                packet.mincosts[i] = (destination, INFINITY)

    def to_layer2(self, packet):
        """Wrapper around the `to_layer2` method of the superclass which
        "poisons" the specified packet before sending it out.

        For more information, see the `poison` method.

        """
        self.poison(packet)
        logger.debug('to_layer2(): poisoned packet {}'.format(packet))
        super().to_layer2(packet)

    def update_and_send(self):
        """Updates the routing table and sends any changes to the neighbors of
        this node.

        """
        V_i = []
        for j in range(len(self.D_i)):
            if j == self.node_id:
                continue
            min_neighbor, min_distance = min(self.D_i[j].items(),
                                             key=lambda e: e[1])
            if min_distance != self.routing_table[j][1]:
                self.routing_table[j] = (min_neighbor, min_distance)
                logger.debug('  distance matrix updated')
                self.log_distances()
                V_i.append((j, min_distance))
        if V_i:
            logger.debug('  sending vector to neighbors: {}'.format(V_i))
            for neighbor in self.neighbors():
                send_pkt = Packet(self.node_id, neighbor, V_i)
                self.to_layer2(send_pkt)
