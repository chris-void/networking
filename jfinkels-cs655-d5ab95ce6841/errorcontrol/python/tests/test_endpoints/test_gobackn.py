# test_gobackn.py - unit tests for the endpoints.gobackn module
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `endpoints.gobackn` module."""
import io

from simulation.datacontainers import Message
from simulation.endpoints.gobackn import GBNSender
from simulation.endpoints.gobackn import GBNReceiver

from ..helpers import LinkedTestSupport

__all__ = ['GBNSenderTest', 'GBNReceiverTest']
"""The names of all the test cases, so that when other modules do `import *
from test_gobackn`, they get the names of all the test cases.

"""


class GBNSenderTest(LinkedTestSupport):
    """Tests for the `GBNSender` class."""

    def setUp(self):
        """Initializes the sender to test."""
        super().setUp()
        self.windowsize = 4
        self.sender = GBNSender(self.windowsize, self.scheduler, 1, 10, 1,
                                self.random)
        self.sender.set_link(self.link)

    def test_from_layer5(self):
        """Tests that messages from layer 5 are queued and sent in order, and
        that messages from layer 5 beyond the window size are queued.

        """
        messages = [Message(str(n)) for n in range(5)]
        for message in messages:
            self.sender.from_layer5(message)
        events = self.get_events()
        self.assertEqual(5, len(events))
        arrival_events = \
            filter(lambda x: x.action == self.destination._from_layer3, events)
        timer_events = \
            filter(lambda x: x.action == self.sender._timer_interrupt, events)
        self.assertEqual(1, len(list(timer_events)))
        self.assertEqual(4, len(list(arrival_events)))
        for message, event in zip(messages, arrival_events):
            self.assertEqual(message.data, event.argument[0].data)

    def test_from_layer3(self):
        """Tests that receiving an ACK bumps up the base sequence number."""
        self.fail('not yet implemented')


class GBNReceiverTest(LinkedTestSupport):
    """Tests for the `GBNReceiver` class."""

    def setUp(self):
        """Initializes the receiver to test and creates a temporary file to
        which it writes its output.

        """
        super().setUp()
        self.outfile = io.StringIO()
        self.receiver = GBNReceiver(self.scheduler, self.outfile)
        self.receiver.set_link(self.link)

    def tearDown(self):
        """Closes the temporary file used by the receiver."""
        self.outfile.close()

    def test_from_layer3(self):
        self.fail('not yet implemented')
