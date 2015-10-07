# runner.py - convenience functions for running a simulation
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides a convenience function for running a simulation with a particular
set of parameters.

"""
from .simulation import Simulation

def mean(l):
    """Returns the arithmetic mean of the numbers in the specified list."""
    if len(l) == 0:
        return -1
    return sum(l) / len(l)

class Results(object):
    pass

def run_parameterized_simulation(*args, **kw):
    """Runs a single instance of the simulation with the specified set of
    parameters.

    The positional and keyword arguments are the same as for the constructor
    for the `simulation.simulation.Simulation` class.

    Returns a `Results` object, which has the following attributes:

    * `throughput` - number of packets (corrupt, duplicate, etc.) received over
      total simulation time
    * `goodput` - number of correct, non-duplicate packets received over total
      simulation time
    * `rtts` - round-trip times for each of the packets
    * `mean_rtt` - mean round-trip time over all packets
    * `num_retransmitted` - number of retransmitted packets by the sender
    * `num_corrupt` - number of corrupted packets received by both the sender
      and the receiver
    * `num_lost` - number of packets lost in the channel

    """
    simulation = Simulation(*args, **kw)
    simulation.run()
    result = Results()
    result.throughput = simulation.throughput()
    result.goodput = simulation.goodput()
    result.rtts = simulation.round_trip_times()
    result.mean_rtt = mean(result.rtts)
    result.num_retransmitted = simulation.num_retransmitted()
    result.num_corrupt = simulation.num_corrupt()
    result.num_lost = simulation.num_lost()
    result.num_sent = simulation.num_sent()
    return result
