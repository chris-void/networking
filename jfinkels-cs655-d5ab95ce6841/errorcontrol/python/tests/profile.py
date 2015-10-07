# profile.py - runs a profiler on the simulation for debugging purposes
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Profiles a single run of a simulation and prints the results, for debugging
purposes.

"""
import cProfile
import logging
from string import ascii_lowercase as LETTERS

from simulation.datacontainers import MAX_DATA_SIZE
from simulation.simulation import Simulation

def run_simulation(*args, **kw):
    """Runs a simulation by passing on the positional and keyword arguments
    directly to the constructor for `simulation.simulation.Simulation`.

    Asserts that the output is in alphabetical order.

    """
    simulation = Simulation(*args, **kw)
    simulation.run()
    output = simulation.output.split()
    logging.critical('lines received: {}'.format(len(output)))
    logging.critical(output)
    for i in range(len(output)):
        assert (LETTERS[i % 26]) * MAX_DATA_SIZE == output[i]

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    cProfile.run("run_simulation(500, protocol='GBN', loss_probability=0.2,"
                 " corruption_probability=0.2)", sort='time')
