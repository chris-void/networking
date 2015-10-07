# bases.py - abstract base classes for routing nodes
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides the abstract base classes for routing nodes."""
import copy
import logging

from ..datacontainers import Packet
from ..random import next_double

logger = logging.getLogger(__name__)
"""The logger for this module."""

INFINITY = float('inf')
"""The IEEE 754 floating point value for infinity.

This is used as a sentinel value in comparisons for uninitialized distances.

"""


class Node(object):
    """A node which can participate in a routing network.

    The `initialize` method must be called before any routing can be performed.

    Subclasses must override and implement the `from_layer2` and
    `link_changed` methods.

    """

    def __init__(self, scheduler, node_id, initial_link_costs, total_nodes):
        """Instantiates this routing node with the specified node ID number
        and dictionary of initial link costs (a map from node ID integer to
        cost as an integer) to each of the neighbors of this node.

        `total_nodes` is the total number of nodes in the graph.

        """
        self.node_id = node_id
        self.scheduler = scheduler
        self.total_nodes = total_nodes
        self.link_costs = copy.deepcopy(initial_link_costs)

        # costs is a two-dimensional array representing a table in which the
        # first dimension is the "via" node, and the second is the destination
        self.costs = [[INFINITY] * total_nodes for n in range(total_nodes)]
        for neighbor, cost in self.link_costs.items():
            self.costs[self.node_id][neighbor] = cost

    def neighbors(self):
        """Returns all neighbors of this node (that is, other nodes which do
        not have cost infinity).

        """
        result = [n for n, c in self.link_costs.items()
                  if c != INFINITY and n != self.node_id]
        return result

    def initialize(self, all_nodes):
        """Provides this node with a mapping from node ID integer to `Node`
        instance for all nodes in the graph in which this node lives, and
        sends the initial distance vectors to the neighbors of this node.

        `all_nodes` is a dictionary mapping ID numbers to `Node`
        instances. The length of `all_nodes` must equal `total_nodes` as
        specified in the constructor for this class.

        """
        self.nodes = all_nodes.copy()
        mycosts = copy.deepcopy(self.costs[self.node_id])
        for neighbor in self.neighbors():
            packet = Packet(self.node_id, neighbor, mycosts)
            self.to_layer2(packet)

    def from_layer2(self, packet):
        """Updates the routing table of this node due to `packet`, the received
        `Packet` instance.

        This function was called `rtupdate` in the original code.

        Subclasses must override and implement this method.

        """
        pass

    def link_changed(self, link_id, newcost):
        """Updates the routing table of this node due to a change in the cost
        of the link specified by `link_id` (an integer) to the new cost given
        by `newcost` (also an integer).

        This function was called `linkhandler` in the original code.

        Subclasses must override and implement this method.

        """
        pass

    def last_arrival_time(self, dest_id):
        """Returns the time of the latest packet arrival event on the node
        with the specified ID number, or the current simulation time if there
        is no packet arrival event scheduled on that node.

        If `dest_id` is not the ID number of a node which is a known neighbor
        of this node, a `KeyError` will be raised.

        """
        filter_func = lambda e: e.action == self.nodes[dest_id].from_layer2
        arrival_events = list(filter(filter_func, self.scheduler.queue))
        if len(arrival_events) > 0:
            return max(arrival_events).time
        return self.get_time()

    def get_time(self):
        """Returns the current simulation time from the scheduler."""
        return self.scheduler.timefunc()

    def schedule_arrival(self, packet):
        """Schedules `packet` to arrive on its destined node."""
        last_time = self.last_arrival_time(packet.dest)
        node = self.nodes[packet.dest]
        delay = 2 * next_double()
        e = self.scheduler.enterabs(last_time + delay, 1, node.from_layer2,
                                    (packet, ))

    def sanity_check(self, packet):
        """Returns `True` if and only if the specified packet meets some
        sanity requirements:

        * the source and destination ID must be in the interval [0,
          `total_nodes`),
        * the source must not equal the destination, and
        * the source and the destination must be adjacent

        """
        if packet.source < 0 or packet.source >= self.total_nodes:
            logger.warn('illegal source ID, droping packet {}'.format(packet))
            return False
        if packet.dest < 0 or packet.dest >= self.total_nodes:
            logger.warn('illegal dest ID, droping packet {}'.format(packet))
            return False
        if packet.source == packet.dest:
            logger.warn('src equals dest, dropping packet {}'.format(packet))
            return False
        if self.link_costs[packet.dest] == INFINITY:
            logger.warn('source and dest not connected, dropping packet {}'
                        .format(packet))
            return False
        return True

    def to_layer2(self, packet):
        """Sends `packet` to layer 2, which schedules an arrival event on the
        node for which the packet is destined.

        """
        if not self.sanity_check(packet):
            logger.warn('failed sanity check')
            return
        new_packet = copy.deepcopy(packet)
        self.schedule_arrival(packet)

    def pretty_print(self):
        """Pretty prints the distance table of this node to stdout."""
        other_nodes = list(range(self.total_nodes))
        del other_nodes[self.node_id]
        print("                via     ")
        print("   D{} |    {}".format(self.node_id,
                                      '    '.join(map(str, other_nodes))))
        print("  ----|-----------------")
        first = True
        for n in other_nodes:
            if first:
                print('dest', end='')
                first = False
            else:
                print('    ', end='')
            print(" {}|  {}"
                  .format(n, '   '.join(['{:3}'] * 3))
                  .format(*(self.costs[n][i]
                            for i in range(len(self.costs[n])))))

    def __str__(self):
        """Returns a human-readable representation of this node."""
        return 'Node[id {}]'.format(self.node_id)
