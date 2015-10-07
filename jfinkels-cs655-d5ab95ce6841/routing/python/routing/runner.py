# runner.py - convenience functions for running a simulation
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides a convenience function for running a simulation with a particular
set of parameters.

"""
from .simulation import Simulation


class Results(object):
    """Encapsulates the measured data from a single run of a simulation with a
    specified set of parameters.

    """
    pass


def run_parameterized_simulation(*args, **kw):
    """Runs a single instance of the simulation with the specified set of
    parameters.

    The positional and keyword arguments are the same as for the constructor
    for the `routing.simulation.Simulation` class.

    Returns a `Results` object, which has the following attributes:


    """
    simulation = Simulation(*args, **kw)
    simulation.run()
    result = Results()
    return result
