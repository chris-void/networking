# alternatingbit.py - the sender and receiver for the "alternating bit" protocol
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides the sender and receiver for the "alternating bit" protocol."""
import logging

from .bases import Receiver
from .bases import Sender

logger = logging.getLogger(__name__)
"""The logger for this module."""


class State:
    """Enumerates possible states for the sender."""
    WAIT0 = 0
    """Waiting for message 0 from layer 5."""
    WAIT1 = 1
    """Waiting for message 1 from layer 5."""
    WAITACK0 = 2
    """Waiting for ACK 0."""
    WAITACK1 = 3
    """Waiting for ACK 1."""


class ABSender(Sender):
    """Sender for the alternating bit protocol."""

    def __init__(self, *args, **kw):
        """Initializes the current state to `State.WAIT0` (waiting for message
        0 from layer 5), passing all positional and keyword arguments on to
        the constructor of the superclass.

        """
        super().__init__(*args, **kw)
        self.state = State.WAIT0
        self.waiting_messages = []

    def from_layer5(self, message):
        """Creates a packet from the specified message received from layer 5
        and queues it for transmission, or sends it immediately if there are no
        other messages waiting.

        """
        logger.debug('ABSender.from_layer5(): receiving message from layer 5')
        self.waiting_messages.append(message)
        logger.debug(self.waiting_messages)
        if len(self.waiting_messages) == 1:
            logger.debug('ABSender.from_layer5(): there are no other messages'
                         ' waiting to be sent, so send this one')
            self.send_waiting_message()

    def send_waiting_message(self):
        """Sends the message at the head of the queue of messages waiting to be
        sent.

        """
        message = self.waiting_messages[0]
        if self.state in (State.WAITACK0, State.WAITACK1):
            logger.warn('ABSender.send_waiting_message(): queuing message from'
                        ' layer 5 because we are still waiting for an ACK'
                        ' (message {})'.format(message.data))
            return
        data = message.data
        acknum = 0
        if self.state == State.WAIT0:
            seqnum = 0
            next_state = State.WAITACK0
        elif self.state == State.WAIT1:
            seqnum = 1
            next_state = State.WAITACK1
        else:
            logger.error('ABSender.send_waiting_message(): sender in unknown'
                         ' state')
            return
        self.packet_to_send = self.make_packet(seqnum, acknum, data)
        self.to_layer3(self.packet_to_send)
        self.start_timer(self.timeout)
        self.state = next_state

    def from_layer3(self, packet):
        logger.debug('from_layer3(): sender received ACK {}'.format(packet))
        if self.is_corrupt(packet):
            logger.error('  but it is corrupt')
            self.num_corrupt += 1
            return
        if self.state == State.WAITACK0:
            logger.debug('  waiting for ACK0')
            expecting_acknum = 0
            next_state = State.WAIT1
        elif self.state == State.WAITACK1:
            logger.debug('  waiting for ACK1')
            expecting_acknum = 1
            next_state = State.WAIT0
        else:
            logger.warn('from_layer3(): received a packet from layer 3 while'
                        ' waiting for a message from layer 5')
            return
        if packet.acknum != expecting_acknum:
            logger.warn('from_layer3(): received ACK for wrong packet number;'
                        ' expecting {}, received {}'.format(packet.acknum,
                                                            expecting_acknum))
            return
        logger.debug('  stopping timer...')
        self.stop_timer()
        self.state = next_state
        if len(self.waiting_messages) > 0:
            self.waiting_messages.pop(0)
        if len(self.waiting_messages) > 0:
            logger.debug('ABSender.from_layer3(): there are messages in the'
                         ' queue to send, so send the next one')
            self.send_waiting_message()
        logger.debug('from_layer3(): received ACK {}'.format(packet.acknum))

    def timer_interrupt(self):
        """Handle a timer interrupt by resending the packet for whose ACK this
        sender is waiting.

        """
        if self.state in (State.WAIT0, State.WAIT1):
            logger.warn('timeout while waiting for message from layer 5')
            return
        logger.debug('timer_interrupt(): resending packet {}'
                     .format(self.packet_to_send))
        self.to_layer3(self.packet_to_send)
        self.start_timer(self.timeout)


class ABReceiver(Receiver):
    """Receiver for the alternating bit protocol."""

    def __init__(self, *args, **kw):
        """Initializes the current state to `State.WAIT0` (waiting for packet
        0 from the sender), passing all positional and keyword arguments on to
        the constructor of the superclass.

        """
        super().__init__(*args, **kw)
        self.state = State.WAIT0
        self.ack_to_send = None

    def from_layer3(self, packet):
        if self.state == State.WAIT0:
            expecting_seqnum = 0
            next_state = State.WAIT1
        elif self.state == State.WAIT1:
            expecting_seqnum = 1
            next_state = State.WAIT0
        else:
            logger.error('from_layer3(): receiver in unknown state')
            return
        if packet.seqnum != expecting_seqnum:
            logger.error('from_layer3(): received packet with wrong sequence'
                         ' number; expecting {}, received {}'
                         .format(expecting_seqnum, packet.seqnum))
            if self.ack_to_send is not None:
                self.to_layer3(self.ack_to_send)
            return
        if self.is_corrupt(packet):
            logger.error('from_layer3(): received corrupt packet: {}'
                         .format(packet))
            return
        self.to_layer5(packet.data)
        logger.debug('from_layer3(): delivered data for packet {}'
                     .format(packet))
        self.state = next_state
        self.ack_to_send = self.make_packet(0, packet.seqnum, '')
        self.to_layer3(self.ack_to_send)
