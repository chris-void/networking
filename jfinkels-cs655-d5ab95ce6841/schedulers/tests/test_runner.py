# test_runner.py - unit tests for the runner module
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Unit tests for the runner module."""
from random import Random
from unittest import TestCase

from SimPy.Simulation import Simulation
from SimPy.Simulation import infinity

from simulation.analysis import measured_throughput
from simulation.endpoints import TrafficManager
from simulation.endpoints import TrafficSink
from simulation.endpoints import TrafficSource
from simulation.runner import run_parameterized_simulation
from simulation.schedulers import FIFO
from simulation.schedulers import RoundRobin

__all__ = ['RunnerTest', 'MiscTest']


class RunnerTest(TestCase):
    """Test for the functions in the runner module."""

    def test_run_parameterized_simulation(self):
        """Tests that running a parameterized simulation works."""
        run_parameterized_simulation(max_packets=1000, scheduler='DRR')

    def test_run_parameterized_simulation_bad_argument(self):
        """Tests that a run_parameterized_simulation doesn't raise an
        exception, unless a bogus argument is provided.

        """
        run_parameterized_simulation(max_packets=1000, scheduler='FIFO')
        run_parameterized_simulation(max_packets=1000, scheduler='RR')
        run_parameterized_simulation(max_packets=1000, scheduler='DRR')
        with self.assertRaises(ValueError):
            run_parameterized_simulation(scheduler='bogus')

    def test_throughput_ratio_almost_one(self):
        """Tests that each traffic source is able to achieve throughput near
        expected throughput when run with a FIFO scheduler and no other
        competing traffic sources.

        """
        result = run_parameterized_simulation(telnet=1, ftp=0, rogue=0,
                                              max_packets=2000)
        self.assertAlmostEqual(1.0, result[0].throughput_ratio, delta=0.01)

        result = run_parameterized_simulation(telnet=0, ftp=1, rogue=0,
                                              max_packets=2000)
        self.assertAlmostEqual(1.0, result[0].throughput_ratio, delta=0.01)

        result = run_parameterized_simulation(telnet=0, ftp=0, rogue=1,
                                              max_packets=2000)
        self.assertAlmostEqual(1.0, result[0].throughput_ratio, delta=0.01)

    def test_latency_increases_with_load_fifo(self):
        """Tests that an increase in load corresponds to an increase in
        latency for each source, using a FIFO scheduler.

        """
        results5 = run_parameterized_simulation(telnet=1, ftp=1, rogue=1,
                                                max_packets=1000,
                                                total_offered_load=0.5,
                                                scheduler='FIFO')
        results10 = run_parameterized_simulation(telnet=1, ftp=1, rogue=1,
                                                 max_packets=1000,
                                                 total_offered_load=1.0,
                                                 scheduler='FIFO')
        results20 = run_parameterized_simulation(telnet=1, ftp=1, rogue=1,
                                                 max_packets=1000,
                                                 total_offered_load=2.0,
                                                 scheduler='FIFO')
        for i in range(3):
            self.assertLess(results5[i].mean_latency,
                            results10[i].mean_latency)
            self.assertLess(results10[i].mean_latency,
                            results20[i].mean_latency)

    def test_latency_increases_with_load_rr(self):
        """Tests that an increase in load corresponds to an increase in
        latency for each source, using a round-robin scheduler.

        """
        results5 = run_parameterized_simulation(telnet=1, ftp=1, rogue=1,
                                                max_packets=1000,
                                                total_offered_load=0.5,
                                                scheduler='RR')
        results10 = run_parameterized_simulation(telnet=1, ftp=1, rogue=1,
                                                 max_packets=1000,
                                                 total_offered_load=1.0,
                                                 scheduler='RR')
        results20 = run_parameterized_simulation(telnet=1, ftp=1, rogue=1,
                                                 max_packets=1000,
                                                 total_offered_load=2.0,
                                                 scheduler='RR')
        for i in range(3):
            self.assertLess(results5[i].mean_latency,
                            results10[i].mean_latency)
            self.assertLess(results10[i].mean_latency,
                            results20[i].mean_latency)

    def test_latency_increases_with_load_drr(self):
        """Tests that an increase in load corresponds to an increase in
        latency for each source, using a round-robin scheduler.

        """
        results5 = run_parameterized_simulation(telnet=0, ftp=1, rogue=0,
                                                max_packets=1500, seed=1234,
                                                total_offered_load=0.5,
                                                scheduler='DRR')
        results10 = run_parameterized_simulation(telnet=0, ftp=1, rogue=0,
                                                 max_packets=1500, seed=1234,
                                                 total_offered_load=1.0,
                                                 scheduler='DRR')
        results20 = run_parameterized_simulation(telnet=0, ftp=1, rogue=0,
                                                 max_packets=1500, seed=1234,
                                                 total_offered_load=2.0,
                                                 scheduler='DRR')
        self.assertLess(results5[0].mean_latency,
                        results10[0].mean_latency)
        self.assertLess(results10[0].mean_latency,
                        results20[0].mean_latency)


class MiscTest(TestCase):
    """Miscellaneous tests."""

    def test_split_load_fifo(self):
        """Tests that two sources with 1/3 and 2/3 the total load should have
        proportional throughputs through a first-in, first-out scheduler.

        """
        simulation = Simulation()
        scheduler = FIFO()
        rng = Random(1234)
        manager = TrafficManager(2000)
        source0 = TrafficSource(scheduler, 0, 1000, 1, manager,
                               random_number_generator=rng, sim=simulation)
        source1 = TrafficSource(scheduler, 0, 1000, 2, manager,
                               random_number_generator=rng, sim=simulation)
        sink = TrafficSink(scheduler, manager, sim=simulation)
        simulation.initialize()
        source0.start()
        source1.start()
        sink.start()
        simulation.simulate(until=infinity)

        throughput1 = measured_throughput(source0, sink)
        throughput2 = measured_throughput(source1, sink)
        self.assertAlmostEqual(2 * throughput1, throughput2, delta=0.001)

    def test_split_load_rr(self):
        """Tests that two sources with 1/3 and 2/3 the total load should have
        proportional throughputs through a round-robin scheduler.

        """
        simulation = Simulation()
        scheduler = RoundRobin()
        rng = Random(1234)
        manager = TrafficManager(2000)
        source0 = TrafficSource(scheduler, 0, 1000, 1, manager,
                               random_number_generator=rng, sim=simulation)
        source1 = TrafficSource(scheduler, 0, 1000, 2, manager,
                               random_number_generator=rng, sim=simulation)
        sink = TrafficSink(scheduler, manager, sim=simulation)
        simulation.initialize()
        source0.start()
        source1.start()
        sink.start()
        simulation.simulate(until=infinity)

        throughput1 = measured_throughput(source0, sink)
        throughput2 = measured_throughput(source1, sink)
        self.assertAlmostEqual(2 * throughput1, throughput2, delta=0.001)

    def test_split_load_drr(self):
        """Tests that two sources with 1/3 and 2/3 the total load should have
        proportional throughputs through a deficit round-robin scheduler.

        """
        simulation = Simulation()
        scheduler = RoundRobin()
        rng = Random(1234)
        manager = TrafficManager(2000)
        source0 = TrafficSource(scheduler, 0, 1000, 1, manager,
                               random_number_generator=rng, sim=simulation)
        source1 = TrafficSource(scheduler, 0, 1000, 2, manager,
                               random_number_generator=rng, sim=simulation)
        sink = TrafficSink(scheduler, manager, sim=simulation)
        simulation.initialize()
        source0.start()
        source1.start()
        sink.start()
        simulation.simulate(until=infinity)

        throughput1 = measured_throughput(source0, sink)
        throughput2 = measured_throughput(source1, sink)
        self.assertAlmostEqual(2 * throughput1, throughput2, delta=0.001)
