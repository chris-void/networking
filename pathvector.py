# pathvector.py - node which uses the path vector routing protocol
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides the node class for the path vector protocol."""
import copy
import logging

from ..datacontainers import Packet
from .bases import INFINITY
from .bases import Node

STAR = None
"""Represents a null head of a path."""

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


class PathVectorNode(Node):
    """Uses a mixed distance vector/path vector strategy implemented with the
    modified distributed Bellman-Ford algorithm to determine the shortest path
    to other nodes in the graph.

    """

    def __init__(self, *args, **kw):
        """Initializes the routing table and distance matrix for this node."""
        super().__init__(*args, **kw)
        # HACK logger is global to allow wrapping logger.debug
        #global logger
        #logger = Logger(self.scheduler, _logger)
        # key is destination (j), value is triple (preferred neighbor (P_ij),
        # shortest distance (RDIST_i_ofj), HEAD_i_ofj)
        self.routing_table = dict([(d, (STAR, INFINITY, STAR))
                                   for d in range(self.total_nodes)])
        self.d_i = self.link_costs
        # first dimension is destination, second is "via", entry is pair
        # (distance from i to j via k (D_ij_k), head of that path (h_ij_k))
        self.D_i = [dict((n, (INFINITY, STAR)) for n in self.neighbors())
                    for m in range(self.total_nodes)]
        for k in self.neighbors():
            self.routing_table[k] = (k, self.d_i[k], self.node_id)
        self.routing_table[self.node_id] = (STAR, 0, STAR)
        for n in self.neighbors():
            self.D_i[n][n] = (self.d_i[n], self.node_id)

    def path_to(self, j):
        """Returns a list of nodes representing the path from this node to the
        destination node `j`.

        """
        #logger.debug('path_to(): {}'.format(j))
        path = []
        c = j
        path.append(c)
        while c != self.node_id:
            #logger.debug('   path: {}'.format(path))
            path.append(c)
            c = self.routing_table[c][2]
        return reversed(path)

    def from_layer2(self, packet):
        """Updates the distance matrix with the new distances specified in the
        packet, updates the routing table if necessary due to changes in the
        distance matrix, and sends any changes to the neighbors of this node.

        """
        #logger.debug('from_layer2(): {}'.format(packet))
        i, k, V_ki = packet.dest, packet.source, packet.mincosts
        for (j, D_kj, h_kofj) in V_ki:
            if j == i:
                continue
            if h_kofj is None:
                h_kofj = self.node_id
            #logger.debug('  copying cost from neighbor {} via {}: ({}, {})'.format(j, k, D_kj, h_kofj))
            self.D_i[j][k] = (D_kj + self.d_i[k], h_kofj)
        self.log_routing_table()
        self.log_distances()
        self.update_and_send(k)

    def initialize(self, all_nodes):
        """Provides this node with a mapping from node ID integer to `Node`
        instance for all nodes in the graph in which this node lives, and
        sends the initial distance vectors to the neighbors of this node.

        `all_nodes` is a dictionary mapping ID numbers to `Node`
        instances. The length of `all_nodes` must equal `total_nodes` as
        specified in the constructor for this class.

        """
        logger.debug('initialize(): node {}'.format(self.node_id))
        self.nodes = all_nodes.copy()
        mycosts = copy.deepcopy(self.routing_table_to_vector())
        for neighbor in self.neighbors():
            logger.debug('initialize():   sending to neighbor {}'.format(neighbor))
            packet = Packet(self.node_id, neighbor, mycosts)
            self.to_layer2(packet)

    def in_path(self, neighbor, dest):
        """Returns `True` if and only if the specified neighbor is on the
        currently known path to `dest` (according to the routing table).

        """
        return neighbor in self.path_to(dest)

    def is_minimum_of_row(self, c, b):
        """Returns `True` if and only if the distance currently in the distance
        table for destination `c` via neighbor `b` is the minimum of row `c`.

        """
        minimum_of_row = min(self.D_i[c].values(), key=lambda e: e[0])
        return minimum_of_row == self.D_i[c][b][0]

    def link_down(self, link_id):
        """Updates the distance matrix and routing table due to a failure of
        the link between this node and the specified neighbor node ID.

        `link_id` is the ID of the neighbor whose link has failed.

        Pre-condition: the specified link was already up.

        """
        k = link_id
        for v in range(self.total_nodes):
            self.D_i[v][k] = (INFINITY, STAR)
        self.update_and_send(k)

    def link_up(self, link_id, cost):
        """Updates the distance matrix and routing table due to the link
        between this node and the neighbor with ID `link_id` becoming active
        with the specified new cost.

        Pre-condition: the specified link was already down.

        """
        i, k = self.node_id, link_id
        d_ik = cost
        V_ki = [(k, d_ik, i)]
        packet = Packet(k, i, V_ki)
        self.from_layer2(packet)
        V_ik = self.routing_table
        packet = Packet(i, k, V_ik)
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
        logger.debug('  Distance table for node {}:'.format(self.node_id))
        for dest, row in enumerate(self.D_i):
            logger.debug('  {}: {}'.format(dest, row))

    def log_routing_table(self):
        """Logs the current routing table at the `DEBUG` level."""
        logger.debug('  Routing table for node {}:'.format(self.node_id))
        for key, row in self.routing_table.items():
            logger.debug('  {}: {}'.format(key, row))

    def minimum_distance_neighbor_in_row(self, j):
        """Returns the neighbor with the minimum distance in row `j` in the
        distance table.

        """
        return min(self.D_i[j].items(), key=lambda e: e[1][0])[0]

    def routing_table_must_change(self, k):
        """Returns `True` if and only if there exists a destination `j` and a
        neighbor `b` such that one of the following conditions is true:

        1. the distance table and the routing table disagree on the distance to
        destination `j` via neighbor `b`, or
        2. `k` is the next hop to the destination `j`.

        Here, `k` is the neighbor from which we received a packet.

        """
        for j in range(self.total_nodes):
            for b in self.neighbors():
                if (self.D_i[j][b][0] < self.routing_table[j][1]
                    or k == self.routing_table[j][0]):
                    return True
        return False

    def routing_table_to_vector(self):
        """Returns a list of triples of the form `(destination,
        distance_to_dest, head_of_path)`, which can be sent to other nodes in a
        packet.

        """
        return [(j, d, h) for j, (p, d, h) in self.routing_table.items()]

    def rt_update(self):
        """Updates the distances in the routing table by using the distances
        from the distance table.

        """
        determined = dict([(dict, False) for d in range(self.total_nodes)])
        # TODO should this be `for j in filter(lambda x: x, dest_determined)`?
        for j in determined:
            logger.debug("rt_update(): j {}".format(j))
            if j == self.node_id:
                logger.debug('         skipping this node')
                continue
            if determined[j]:
                logger.debug('         is determined, continuing...')
                continue
            if all(map(lambda e: e == INFINITY, self.D_i[j].values())):
                determined[j] = False
                logger.debug('         has no determined distances in row:')
                logger.debug('     marking as undetermined and continuing...')
                continue
            TV = []
            b = self.minimum_distance_neighbor_in_row(j)
            self.log_distances()
            self.log_routing_table()
            logger.debug('rt_update():   b {}'.format(b))
            #c = h_ij_b
            c = self.D_i[j][b][1]
            TV.append(c)
            logger.debug('rt_update():   c {}'.format(c))
            logger.debug('rt_update():   TV {}'.format(TV))
            while (self.is_minimum_of_row(c, b)
                   and self.D_i[c][b][1] != self.node_id
                   and not determined[self.D_i[c][b][1]]):
                self.log_routing_table()
                self.log_distances()
                logger.debug('rt_update():    c {}'.format(c))
                c = self.D_i[c][b][1]
                TV.append(c)
            if (self.D_i[c][b][1] is None
                or not determined[self.D_i[c][b][1]]
                or not self.is_minimum_of_row(c, b)):
                logger.debug('    not determined or not minimum')
                for n in TV:
                    determined[n] = False
            else:
                logger.debug('    determined and minimum')
                for n in TV:
                    determined[n] = True
                    RDIST_i_j, HEAD_i_j = self.D_i[j][b]
                    P_ij = b
                    self.routing_table[j] = (P_ij, RDIST_i_j, HEAD_i_j)
        # copy routing table to V_i done in from_layer2

    def update_and_send(self, k):
        """Updates the routing table and sends any changes to the neighbors of
        this node.

        """
        logger.debug('update_and_send()')
        V_i = []
        if self.routing_table_must_change(k):
            self.rt_update()
            V_i = self.routing_table_to_vector()
        if V_i:
            for b in self.neighbors():
                V_ib = []
                for t in V_i:
                    j, rdist_iofj, head_iofj = t
                    if self.in_path(b, j):
                        V_ib.append((j, INFINITY, STAR))
                    else:
                        V_ib.append(t)
                send_pkt = Packet(self.node_id, b, V_ib)
                self.to_layer2(send_pkt)
