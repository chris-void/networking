# test_bases.py - unit tests for the endpoint.bases module
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `endpoints.bases` module."""
import io

from simulation.datacontainers import Message
from simulation.datacontainers import Packet
from simulation.endpoints.bases import Endpoint
from simulation.endpoints.bases import Receiver
from simulation.endpoints.bases import Sender

from ..helpers import LinkedTestSupport
from ..helpers import TestSupport

__all__ = ['EndpointTest', 'SenderTest', 'ReceiverTest']
"""The names of all the test cases, so that when other modules do `import *
from test_bases`, they get the names of all the test cases.

"""


class EndpointTest(LinkedTestSupport):
    """Tests for the `Endpoint` class."""

    def setUp(self):
        """Initializes the endpoint to test with a link over which to send
        messages.

        """
        super().setUp()
        self.endpoint = Endpoint(self.scheduler)
        self.endpoint.set_link(self.link)

    def test_make_packet(self):
        """Test for creating a packet."""
        seqnum, acknum, msg = 12, 34, '5678'
        checksum = self.endpoint.checksum(seqnum, acknum, msg)
        expected_packet = Packet(seqnum, acknum, checksum, msg)
        observed_packet = self.endpoint.make_packet(seqnum, acknum, msg)
        self.assertEqual(expected_packet, observed_packet)

    def test_to_layer3(self):
        """Tests that delivering a packet to layer 3 sends it along the link.

        """
        packet = Packet(0, 0, 0, 'foo')
        self.endpoint.to_layer3(packet)
        events = self.get_events()
        self.assertEqual(1, len(events))
        event = events[0]
        self.assertGreater(event.time, self.scheduler.timefunc())
        self.assertEqual(self.destination._from_layer3, event.action)
        self.assertEqual(packet, event.argument[0])


class SenderTest(LinkedTestSupport):
    """Tests for the `Sender` class."""

    def setUp(self):
        """Initializes the sender to test."""
        super().setUp()
        self.sender = Sender(self.scheduler, 1, 10, 1, self.random)
        self.sender.set_link(self.link)

    def test__from_layer5(self):
        """Tests that this wrapper around the `from_layer5` function
        increments the number of sent messages and schedules another new
        message arrival (if the number of sent messages has not exceeded the
        maximum number of allowed messages.

        """
        for i in range(10):
            self.assertEqual(i, len(self.get_events()))
            self.assertEqual(i, self.sender.num_sent)
            self.sender._from_layer5(Message('foo'))
        self.assertEqual(0, len(self.get_events()))
        self.assertEqual(10, self.sender.num_sent)
    
    def test_generate_next_arrival(self):
        """Tests that a new message arrival from layer 5 is correctly
        scheduled.

        """
        generated_event = self.sender.generate_next_arrival()
        events = self.get_events()
        scheduled_event = events[0]
        self.assertEqual(1, len(events))
        self.assertEqual(generated_event, scheduled_event)
        self.assertEqual('a' * 20, scheduled_event.argument[0].data)

    def test_start_timer(self):
        """Tests that the `start_timer` function schedules a timer interrupt
        event, unless one is already scheduled.

        """
        events = self.get_events()
        self.assertEqual(0, len(events))
        generated_event = self.sender.start_timer(10)
        events = self.get_events()
        scheduled_event = events[0]
        self.assertEqual(1, len(events))
        self.assertEqual(generated_event, scheduled_event)

    def test_stop_timer(self):
        """Tests that the `stop_timer` function cancels any existing scheduled
        timer interrupt events.

        """
        generated_event = self.sender.start_timer(10)
        self.sender.stop_timer()
        events = self.get_events()
        self.assertEqual(0, len(events))


class ReceiverTest(TestSupport):
    """Tests for the `Receiver` class."""

    def setUp(self):
        """Opens a temporary file to which the receiver object will output
        received messages.

        """
        super().setUp()
        self.outfile = io.StringIO()
        self.receiver = Receiver(self.scheduler, self.outfile)

    def tearDown(self):
        """Closes the temporary outfile and unlinks the filename."""
        self.outfile.close()

    def test_to_layer5(self):
        """Tests that the receiver correctly outputs received messages to a
        file.

        """
        self.receiver.to_layer5('foo')
        self.assertEqual('foo\n', self.outfile.getvalue())
