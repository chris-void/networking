# test_selectiverepeat.py - unit tests for the endpoints.selectiverepeat module
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `endpoints.selectiverepeat` module."""
from simulation.datacontainers import Message
from simulation.datacontainers import Packet
from simulation.endpoints.selectiverepeat import SRSender
from simulation.endpoints.selectiverepeat import SRReceiver

from ..helpers import LinkedTestSupport

__all__ = ['SRSenderTest', 'SRReceiverTest']
"""The names of all the test cases, so that when other modules do `import *
from test_selectiverepeat`, they get the names of all the test cases.

"""


class SRSenderTest(LinkedTestSupport):
    """Tests for the `SRSender` class."""
    pass


class SRReceiverTest(LinkedTestSupport):
    """Tests for the `SRReceiver` class."""
    pass
