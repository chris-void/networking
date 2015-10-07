# runner.py - provides a convenience function for running the simulation
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Provides convenience functions for running simulations with a specific set
of parameters.

The main function provided by this module is the `run_parameterized_simulation`
function. The arguments provide a very specific set of parameters under which
to run a simulation. It returns statistics for each traffic source after the
simulation has terminated.

"""
import logging
import random

from SimPy.Simulation import infinity
from SimPy.Simulation import Simulation as _Simulation

from analysis import PipelineStatistics as Stats
from endpoints import OUTPUT_LINK_RATE
from endpoints import TrafficManager
from endpoints import TrafficSink
from endpoints import TrafficSource
from schedulers import DeficitRoundRobin
from schedulers import FIFO
from schedulers import RoundRobin

LOG_FORMAT = '[%(levelname)s] %(message)s'
"""The formatting string for logged messages."""


class Simulation(object):
    """An encapsulation of a single run of a simulation with a specific set of
    traffic sources and traffic sinks.

    The `run` method must be called only once. After that, its behavior is
    undefined.

    """

    def __init__(self, sources, sinks, simulation):
        """Instantiates and initializes the SimPy `Simulation` object with the
        given traffic sources and sinks.

        `simulation` is the SimPy `simulation` object which controls the
        simulation. It will be initialized in this class, so the `initialize`
        function should **not** be called by code which uses this class.

        `sources` is a list of traffic sources, and `sinks` is a list of
        traffic sinks. Both must be non-empty. It is strongly recommended that
        all endpoints in these two lists have access to the same
        `endpoints.TrafficManager` object, which controls how many packets have
        been generated and when the simulation ends.

        """
        self.simulation = simulation
        self.sources = sources
        self.sinks = sinks

    def run(self):
        """Runs the simulation until all packets have been generated and
        dequeued, and returns statistics for each traffic source.

        The returned dictionary is a mapping from traffic source ID to
        `analysis.PipelineStatistics` object.

        """
        self.simulation.initialize()
        for endpoint in self.sources + self.sinks:
            endpoint.start()
        self.simulation.simulate(until=infinity)
        sink = self.sinks[0]
        return dict([(src.source_id, Stats(src, sink)) for src in self.sources])


class TelnetSource(TrafficSource):
    """A traffic source representing a telnet packet generator."""

    def __init__(self, scheduler, source_id, manager, rate, *args, **kw):
        """Creates a traffic source with an average packet size of 512 bits.

        Passes on the positional and keyword arguments to the constructor of
        the superclass.

        """
        super(TelnetSource, self).__init__(scheduler, source_id, 512, rate,
                                           manager, *args, **kw)
        self.log('creating telnet source {0}'.format(self.source_id))


class FTPSource(TrafficSource):
    """A traffic source representing an FTP packet generator."""

    def __init__(self, scheduler, source_id, manager, rate, *args, **kw):
        """Creates a traffic source with an average packet size of 8192
        bits.

        Passes on the positional and keyword arguments to the constructor of
        the superclass.

        """
        super(FTPSource, self).__init__(scheduler, source_id, 8192, rate,
                                        manager, *args, **kw)
        self.log('creating FTP source {0}'.format(self.source_id))


class RogueSource(TrafficSource):
    """A rogue traffic source which creates packets of arbitrary size at a
    fixed rate.

    """

    def __init__(self, scheduler, source_id, manager, rate, *args, **kw):
        """Creates a rogue traffic source with an average packet size of 5000
        bits.

        Passes on the positional and keyword arguments to the constructor of
        the superclass.

        """
        super(RogueSource, self).__init__(scheduler, source_id, 5000, rate,
                                          manager, *args, **kw)
        self.log('creating rogue source {0}'.format(self.source_id))


def run_simulation(sources, sinks, simulation):
    """Convenience method which instantiates and runs a `runner.Simulation`
    object with the specified sources and sinks, and returns statistics from
    the run.

    `simulation` is the SimPy `simulation` object which controls the
    simulation. It will be initialized in this function, so the `initialize`
    function should **not** be called by code which uses this function.

    `sources` and `sinks` are the endpoints passed to the constructor of
    `runner.Simulation`. Each must have access to the specified `simulation`,
    by specifiying the `sim` keyword parameter in the constructor of each
    endpoint.

    The returned dictionary is a mapping from traffic source ID to
    `analysis.PipelineStatistics` object.

    """
    simulation = Simulation(sources, sinks, simulation)
    simulation.run()
    return dict([(src.source_id, Stats(src, sinks[0])) for src in sources])


def run_parameterized_simulation(debug=False, scheduler='FIFO', ftp=4,
                                 telnet=6, rogue=1, max_packets=100000,
                                 seed=None, total_offered_load=0.4):
    """Performs and returns the results of a single run of a simulation with
    the specified properties.

    Debugging messages will be shown if `debug` is `True`.

    `scheduler` is a string specifying the type of scheduler to use: `'FIFO'`,
    `'RR'`, or `'DRR'`.

    `rogue`, `ftp`, and `telnet` are the numbers of rogue, FTP, and telnet
    traffic sources which will be used in the simulation, respectively. The
    traffic source ID numbers are assigned in increasing order first to telnet
    sources (if any), then to FTP sources (if any), then to rogue sources (if
    any).

    `total_offered_load` is the total offered load for all traffic sources.

    `seed` is an integer which will be used as the seed to the random number
    generator. If not specified, a random seed will be used.

    The returned dictionary is a mapping from traffic source ID to
    `analysis.PipelineStatistics` object.

    """
    logging_level = logging.INFO
    if debug:
        logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level, format=LOG_FORMAT)

    num_sources = ftp + telnet + rogue
    if scheduler == 'FIFO':
        sched = FIFO()
    elif scheduler == 'RR':
        sched = RoundRobin()
    elif scheduler == 'DRR':
        sched = DeficitRoundRobin()
    else:
        raise ValueError("scheduler argument must be one of the strings"
                         " 'FIFO', 'RR', 'DRR'")

    manager = TrafficManager(max_packets)
    random.seed(seed)
    load_per_source = float(total_offered_load) / num_sources
    normal_rate = load_per_source * OUTPUT_LINK_RATE
    rogue_rate = OUTPUT_LINK_RATE / 2.0
    simulation = _Simulation()

    sources = []
    counter = 0
    for num, clazz, rate in ((telnet, TelnetSource, normal_rate),
                             (ftp, FTPSource, normal_rate),
                             (rogue, RogueSource, rogue_rate)):
        for n in range(0, num):
            sources.append(clazz(sched, counter, manager, rate, random,
                                 sim=simulation))
            counter += 1
    sinks = [TrafficSink(sched, manager, sim=simulation)]
    return run_simulation(sources, sinks, simulation)
