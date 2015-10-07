# gobackn.py - the sender and receiver for the "go back N" protocol
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides the sender and receiver for the "go back N" protocol."""
import logging

from .bases import Receiver
from .bases import Sender

logger = logging.getLogger(__name__)
"""The logger for this module."""


class GBNSender(Sender):
    def __init__(self, windowsize, *args, **kw):
        super().__init__(*args, **kw)
        self.windowsize = windowsize
        self.nextseqnum = 1
        self.incoming_messages = []
        self.window = []
        #self.base = 1
        #self.seqnum_limit = self.windowsize + 1
        #self.sent_packets = [None] * self.seqnum_limit
        #self.num_outstanding = 0

    def from_layer5(self, message):
        if len(self.window) >= self.windowsize:
            self.incoming_messages.append(message)
        else:
            self.dispatch_packet(message)

    def dispatch_packet(self, message):
        packet = self.make_packet(self.nextseqnum, 0, message.data)
        self.to_layer3(packet)
        self.sent_at[packet.seqnum] = self.get_time()
        if len(self.window) == 0:
            self.start_timer(self.timeout)
        self.window.append(packet)
        self.nextseqnum += 1
        
    def index_of(self, seqnum):
        """Returns the index of the packet whose sequence number is `seqnum`
        in the current window, or `-1` if no such packet exists in the window.

        """
        try:
            return list(map(lambda p: p.seqnum, self.window)).index(seqnum)
        except ValueError:
            return -1

    def from_layer3(self, packet):
        if self.is_corrupt(packet):
            return
        logger.debug('SENDER received ack for {}'.format(packet.acknum))
        index = self.index_of(packet.acknum)
        logger.debug('  which is at index {} in window'.format(index))
        while index >= 0:
            old_packet = self.window.pop(0)
            self.received_at[old_packet.seqnum] = self.get_time()
            index -= 1
        logger.debug('  window now has length {}'.format(len(self.window)))
        while (len(self.window) < self.windowsize
               and len(self.incoming_messages) > 0):
            message = self.incoming_messages.pop(0)
            self.dispatch_packet(message)
        # Stop the timer every time, then restart it if there are still
        # unacknowledged packets in the window. This essentially extends the
        # timeout period for these unacknowledged packets, and is necessary to
        # avoid thrashing on the network.
        self.stop_timer()
        if len(self.window) > 0:
            self.start_timer(self.timeout)

    def timer_interrupt(self):
        self.start_timer(self.timeout)
        for packet in self.window:
            self.to_layer3(packet)


class GBNReceiver(Receiver):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.expected_seqnum = 1
        self.ack_to_send = self.make_packet(0, 0, '')

    def from_layer3(self, packet):
        if (not self.is_corrupt(packet)
            and self.expected_seqnum == packet.seqnum):
            self.to_layer5(packet.data)
            self.ack_to_send = self.make_packet(0, self.expected_seqnum, '')
            self.expected_seqnum += 1
        self.to_layer3(self.ack_to_send)
