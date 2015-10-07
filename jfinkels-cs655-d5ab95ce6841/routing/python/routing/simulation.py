# simulation.py - encapsulation for an instance of the simulation
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides a class which encapsulates a single trial of the simulation with a
particular set of parameters.

"""
import logging
import sched

from .protocols.bases import INFINITY
from .random import initialize

LOG_FORMAT = '[%(module)s %(levelname)s] %(message)s'
"""The formatting string for logged messages."""
TO_DEBUG_LEVEL = {-1: logging.ERROR, 0: logging.WARN, 1: logging.INFO,
                   2: logging.DEBUG, 3: logging.DEBUG, 4: logging.DEBUG}
"""Mapping from `trace` simulation parameter to logging level."""
logger = logging.getLogger(__name__)
"""The logger for this module."""


class Timer(object):
    """An object which maintains a current time and which can be delayed."""

    def __init__(self, initial_time=0):
        """Sets the time to initially be `initial_time`."""
        self.time = initial_time

    def delay(self, delay_time):
        """Delays the current simulation by the specified delay."""
        self.time += delay_time

    def get_time(self):
        """Returns the current simulation time."""
        return self.time


class Simulation(Timer):
    """Represents a single instance of the simulation with a specified set of
    parameters.

    After running this simulation with the `run()` function, the time of
    termination can be retrieved by calling the `get_time()` function.

    """

    # TODO add link_costs as an input
    def __init__(self, protocol='DV', trace=2, seed=None, link_changes=False):
        """Initializes the scheduler, the nodes, etc. necessary for the
        simulation.

        `protocol` is a string which must be one of `'DV'` or `'PV'`,
        representing the "distance vector" protocol or the "path vector"
        protocol, respectively.

        `trace` is the level of verbosity of logged messages (higher means
        more verbose).

        `seed`, an integer, is the seed for the pseudo-random number generator.

        If `link_changes` is `True`, then at time 10,000, the link between 0
        and 1 will change to have cost 20, changing back to cost 1 at time
        20,000.

        """
        super().__init__()
        logging.basicConfig(format=LOG_FORMAT, level=TO_DEBUG_LEVEL[trace])
        initialize(seed)
        self.scheduler = sched.scheduler(self.get_time, self.delay)

        link_costs = [[0, 1, 10, 7],
                      [1, 0, 1, INFINITY],
                      [10, 1, 0, 2],
                      [7, INFINITY, 2, 0]]

        if protocol == 'DV':
            from .protocols.distancevector import DistanceVectorNode as Node
        elif protocol == 'PV':
            from .protocols.pathvector import PathVectorNode as Node
        else:
            raise ValueError('unknown protocol {}'.format(protocol))
        self.nodes = {}
        for n, costs in enumerate(link_costs):
            self.nodes[n] = Node(self.scheduler, n, dict(enumerate(costs)),
                                 len(link_costs))

        # this call schedules the first arrival event on the scheduler
        for node in self.nodes.values():
            node.initialize(self.nodes)

        if link_changes:
            node0, node1 = self.nodes[0], self.nodes[1]
            self.scheduler.enterabs(10000, 1, node0.link_changed, (1, 20))
            self.scheduler.enterabs(10000, 1, node1.link_changed, (0, 20))
            self.scheduler.enterabs(20000, 1, node0.link_changed, (1, 1))
            self.scheduler.enterabs(20000, 1, node1.link_changed, (0, 1))

        # uncomment this line to pretty print nodes at regular intervals
        #self.scheduler.enterabs(10, 1, self.pretty_print_nodes, ())

    def pretty_print_nodes(self):
        """Pretty prints all nodes to standard output, for debugging purposes.

        """
        for node in self.nodes.values():
            node.pretty_print()
        if len(list(self.scheduler.queue)) > 0:
            self.scheduler.enter(10, 1, self.pretty_print_nodes, ())

    def run(self):
        """Runs the simulation and prints the routing tables for each node
        after the simulation terminates.

        """
        # the initial arrival events are created on the call to
        # `Node.initialize()` in the constructor
        self.scheduler.run()
        logger.debug('')
        logger.debug('distances and routing tables at termination time')
        logger.debug('')
        logger.debug('entries in the routing table are pairs of the form')
        logger.debug('(next hop node ID, total distance)')
        for node_id, node in self.nodes.items():
            logger.debug('routing table for node {}'.format(node_id))
            node.log_routing_table()
            logger.debug('distance table for node {}'.format(node_id))
            node.log_distances()
