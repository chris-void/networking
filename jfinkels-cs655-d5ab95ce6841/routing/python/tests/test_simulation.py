# test_simulation.py - unit tests for the simulation module
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `simulation` module."""
import logging
import unittest

from routing.simulation import Simulation

__all__ = ['DVSimulationTest']
"""The names of all the test cases, so that when other modules do `import *
from test_simulation`, they get the names of all the test cases.

"""

logger = logging.getLogger(__name__)
"""The logger for this module."""


class DVSimulationTest(unittest.TestCase):
    """Tests for the `Simulation` class with the distance vector routing
    protocol.

    """

    def test_run(self):
        """Tests that the simulation runs without errors."""
        simulation = Simulation(trace=2, seed=1234, link_changes=False)
        simulation.run()
