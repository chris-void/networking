# test_alternatingbit.py - unit tests for the endpoints.alternatingbit module
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides unit tests for the `endpoints.alternatingbit` module."""
import io

from simulation.datacontainers import Message
from simulation.datacontainers import Packet
from simulation.endpoints.alternatingbit import ABReceiver
from simulation.endpoints.alternatingbit import ABSender
from simulation.endpoints.alternatingbit import State

from ..helpers import LinkedTestSupport

__all__ = ['ABSenderTest', 'ABReceiverTest']
"""The names of all the test cases, so that when other modules do `import *
from test_alternatingbit`, they get the names of all the test cases.

"""


class ABSenderTest(LinkedTestSupport):
    """Tests for the `ABSender` class."""

    def setUp(self):
        """Initializes the sender to test."""
        super().setUp()
        self.sender = ABSender(self.scheduler, 1, 10, 1, self.random)
        self.sender.set_link(self.link)

    def test_from_layer5(self):
        """Tests that messages received from layer 5 get sent out as packets
        to the receiver.

        """
        self.sender.from_layer5(Message('foo'))
        self.assertEqual(State.WAITACK0, self.sender.state)
        events = self.get_events()
        self.assertEqual(2, len(events))
        event0, event1 = events
        self.assertEqual(self.sender._timer_interrupt, event0.action)
        self.assertEqual(self.link.destination._from_layer3, event1.action)
        packet = event1.argument[0]
        self.assertFalse(self.destination.is_corrupt(packet))
        self.assertEqual(0, packet.seqnum)

        self.sender.stop_timer()
        self.clear_queue()
        self.sender.waiting_messages = []
        self.sender.state = State.WAIT1

        self.sender.from_layer5(Message('bar'))
        self.assertEqual(State.WAITACK1, self.sender.state)
        events = self.get_events()
        self.assertEqual(2, len(events))
        event0, event1 = events
        self.assertEqual(self.sender._timer_interrupt, event0.action)
        self.assertEqual(self.link.destination._from_layer3, event1.action)
        packet = event1.argument[0]
        self.assertFalse(self.destination.is_corrupt(packet))
        self.assertEqual(1, packet.seqnum)

    def test_from_layer3(self):
        self.sender.state = State.WAITACK0
        self.sender.start_timer(self.sender.timeout)
        self.assertEqual(1, len(self.get_events()))
        packet = Packet(0, 0, self.destination.checksum(0, 0, 'foo'), 'foo')
        self.sender.from_layer3(packet)
        self.assertEqual(State.WAIT1, self.sender.state)
        self.assertEqual(0, len(self.get_events()))

        self.sender.state = State.WAITACK1
        self.sender.start_timer(self.sender.timeout)
        self.assertEqual(1, len(self.get_events()))
        packet = Packet(0, 1, self.destination.checksum(0, 1, 'bar'), 'bar')
        self.sender.from_layer3(packet)
        self.assertEqual(State.WAIT0, self.sender.state)
        self.assertEqual(0, len(self.get_events()))

    def test_from_layer3_corrupt(self):
        """Tests that the sender drops corrupt packets."""
        self.sender.state = State.WAITACK0
        packet = Packet(0, 0, 12345, 'corrupt')
        self.sender.from_layer3(packet)
        self.assertEqual(State.WAITACK0, self.sender.state)

        self.sender.state = State.WAITACK1
        packet = Packet(0, 0, 67890, 'corrupt')
        self.sender.from_layer3(packet)
        self.assertEqual(State.WAITACK1, self.sender.state)

    def test_from_layer3_wrong_acknum(self):
        """Tests that the sender drops ACKs with the wrong number."""
        self.sender.state = State.WAITACK0
        packet = Packet(0, 1, self.destination.checksum(0, 1, 'foo'), 'foo')
        self.sender.from_layer3(packet)
        self.assertEqual(State.WAITACK0, self.sender.state)

        self.sender.state = State.WAITACK1
        packet = Packet(0, 0, self.destination.checksum(0, 0, 'bar'), 'bar')
        self.sender.from_layer3(packet)
        self.assertEqual(State.WAITACK1, self.sender.state)

    def test_timer_interrupt(self):
        """Tests that timer interrupt resends the previously sent packet, if
        the sender is waiting for an ACK.

        """
        seqnum, acknum, msg = 0, 0, 'foo'
        checksum = self.sender.checksum(seqnum, acknum, msg)
        self.sender.packet_to_send = Packet(seqnum, acknum, checksum, msg)

        self.sender.state = State.WAITACK0
        self.sender.timer_interrupt()
        events = self.get_events()
        self.assertEqual(2, len(events))
        event0, event1 = events
        self.assertEqual(self.destination._from_layer3, event1.action)
        self.assertEqual(self.sender.packet_to_send, event1.argument[0])

        self.sender.stop_timer()
        self.clear_queue()
        self.sender.state = State.WAITACK1
        self.sender.timer_interrupt()
        events = self.get_events()
        self.assertEqual(2, len(events))
        event0, event1 = events
        self.assertEqual(self.destination._from_layer3, event1.action)
        self.assertEqual(self.sender.packet_to_send, event1.argument[0])

        self.clear_queue()
        self.sender.state = State.WAIT0
        self.sender.timer_interrupt()
        self.assertEqual(0, len(self.get_events()))


class ABReceiverTest(LinkedTestSupport):
    """Tests for the `ABReceiver` class."""

    def setUp(self):
        """Initializes the receiver to test and creates a temporary file to
        which it writes its output.

        """
        super().setUp()
        self.outfile = io.StringIO()
        self.receiver = ABReceiver(self.scheduler, self.outfile)
        self.receiver.set_link(self.link)

    def tearDown(self):
        """Closes the temporary file used by the receiver."""
        self.outfile.close()

    def test_from_layer3(self):
        """Tests that the receiver delivers non-corrupt packets with the
        correct sequence number only.

        """
        seqnum, acknum, msg = 0, 0, 'foo'
        checksum = self.receiver.checksum(seqnum, acknum, msg)
        packet = Packet(seqnum, acknum, checksum, msg)

        self.receiver.from_layer3(packet)
        self.assertEqual('foo\n', self.outfile.getvalue())
        self.receiver.from_layer3(packet)
        self.assertEqual('foo\n', self.outfile.getvalue())

        # TODO create self.create_packet() function
        seqnum, acknum, msg = 1, 0, 'bar'
        checksum = self.receiver.checksum(seqnum, acknum, msg)
        packet = Packet(seqnum, acknum, checksum, msg)

        self.receiver.from_layer3(packet)
        self.assertEqual('foo\nbar\n', self.outfile.getvalue())
        self.receiver.from_layer3(packet)
        self.assertEqual('foo\nbar\n', self.outfile.getvalue())
