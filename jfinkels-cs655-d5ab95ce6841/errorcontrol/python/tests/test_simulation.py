# test_simulation.py - unit tests for the simulation module
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `simulation` module."""
import logging
from string import ascii_lowercase as LETTERS
import unittest

from simulation.datacontainers import MAX_DATA_SIZE
from simulation.simulation import Simulation

__all__ = ['ABSimulationTest', 'GBNSimulationTest', 'SRSimulationTest']
"""The names of all the test cases, so that when other modules do `import *
from test_simulation`, they get the names of all the test cases.

"""

logger = logging.getLogger(__name__)
"""The logger for this module."""


class TestSupport(unittest.TestCase):
    """Base class for test cases in this module."""

    def run_simulation(self, num_messages, *args, **kw):
        """Runs a simulation with the specified parameters and asserts that the
        output is as expected.

        Pre-condition: `num_messages` is less than 26.

        """
        simulation = Simulation(num_messages=num_messages, *args, **kw)
        simulation.run()
        # split the output into a list of lists of length 26 (for each letter)
        output = simulation.output.split()
        logger.debug('received: {}'.format(output))
        for i in range(len(output)):
            self.assertEqual((LETTERS[i % 26]) * MAX_DATA_SIZE, output[i])
        # HACK it may be the case that not all messages were received, since
        # we increment the counter for number of messages sent when we receive
        # a message from layer 5, but not all need be received when the
        # simulation stops
        if len(output) != num_messages:
            logger.error('expected {} messages, but received {}'
                         .format(num_messages, len(output)))


class ABSimulationTest(TestSupport):
    """Tests for the `Simulation` class with the alternating bit protocol."""

    def test_run_no_errors(self):
        """Tests that the simulation runs correctly with no loss and no
        corruption.

        """
        self.run_simulation(2, protocol='AB', loss_probability=0.,
                            corruption_probability=0.)
        self.run_simulation(25, protocol='AB', loss_probability=0.,
                            corruption_probability=0.)

    def test_run_corruption(self):
        """Tests that the simulation runs correctly with corruption but no
        loss.

        """
        self.run_simulation(2, protocol='AB', loss_probability=0.,
                            corruption_probability=0.5)
        self.run_simulation(25, protocol='AB', loss_probability=0.,
                            corruption_probability=0.5)

    def test_run_loss(self):
        """Tests that the simulation runs correctly with loss but no
        corruption.

        """
        self.run_simulation(2, protocol='AB', loss_probability=0.5,
                            corruption_probability=0.)
        self.run_simulation(25, protocol='AB', loss_probability=0.5,
                            corruption_probability=0.)

    def test_run_loss_and_corruption(self):
        """Tests that the simulation runs correctly with both corruption and
        loss.

        """
        self.run_simulation(2, protocol='AB', loss_probability=0.5,
                            corruption_probability=0.5)
        self.run_simulation(25, protocol='AB', loss_probability=0.5,
                            corruption_probability=0.5)


class GBNSimulationTest(TestSupport):
    """Tests for the `Simulation` class with the "go back N" protocol."""

    def test_run_no_errors(self):
        """Tests that the simulation runs correctly with no loss and no
        corruption.

        """
        self.run_simulation(2, protocol='GBN', loss_probability=0.,
                            corruption_probability=0.)
        self.run_simulation(25, protocol='GBN', loss_probability=0.,
                            corruption_probability=0.)

    def test_run_corruption(self):
        """Tests that the simulation runs correctly with corruption but no
        loss.

        """
        self.run_simulation(2, protocol='GBN', loss_probability=0.,
                            corruption_probability=0.5)
        self.run_simulation(25, protocol='GBN', loss_probability=0.,
                            corruption_probability=0.5)

    def test_run_loss(self):
        """Tests that the simulation runs correctly with loss but no
        corruption.

        """
        self.run_simulation(2, protocol='GBN', loss_probability=0.5,
                            corruption_probability=0.)
        self.run_simulation(25, protocol='GBN', loss_probability=0.5,
                            corruption_probability=0.)

    def test_run_loss_and_corruption(self):
        """Tests that the simulation runs correctly with both corruption and
        loss.

        """
        self.run_simulation(2, protocol='GBN', loss_probability=0.5,
                            corruption_probability=0.5)
        self.run_simulation(25, protocol='GBN', loss_probability=0.5,
                            corruption_probability=0.5)

    def test_run_2(self):
        """Tests that the simulation runs correctly with both corruption and
        loss.

        """
        self.run_simulation(25, protocol='GBN')


class SRSimulationTest(TestSupport):
    """Tests for the `Simulation` class with the "selective repeat" protocol.

    """

    def test_run_no_errors(self):
        """Tests that the simulation runs correctly with no loss and no
        corruption.

        """
        self.run_simulation(2, protocol='SR', loss_probability=0.,
                            corruption_probability=0.)
        self.run_simulation(25, protocol='SR', loss_probability=0.,
                            corruption_probability=0.)

    def test_run_corruption(self):
        """Tests that the simulation runs correctly with corruption but no
        loss.

        """
        self.run_simulation(2, protocol='SR', loss_probability=0.,
                            corruption_probability=0.5)
        self.run_simulation(25, protocol='SR', loss_probability=0.,
                            corruption_probability=0.5)

    def test_run_loss(self):
        """Tests that the simulation runs correctly with loss but no
        corruption.

        """
        self.run_simulation(2, protocol='SR', loss_probability=0.5,
                            corruption_probability=0.)
        self.run_simulation(25, protocol='SR', loss_probability=0.5,
                            corruption_probability=0.)

    def test_run_loss_and_corruption(self):
        """Tests that the simulation runs correctly with both corruption and
        loss.

        """
        self.run_simulation(2, protocol='SR', loss_probability=0.5,
                            corruption_probability=0.5)
        self.run_simulation(25, protocol='SR', loss_probability=0.5,
                            corruption_probability=0.5)

    def test_run_2(self):
        """Tests that the simulation runs correctly with both corruption and
        loss.

        """
        self.run_simulation(25, protocol='SR')
