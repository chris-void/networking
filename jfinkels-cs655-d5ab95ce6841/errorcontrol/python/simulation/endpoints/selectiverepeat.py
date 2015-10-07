# selectiverepeat.py - the sender and receiver for the "selective repeat" protocol
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides the sender and receiver for the "selective repeat" protocol."""
import logging

from .bases import Receiver
from .bases import Sender

logger = logging.getLogger(__name__)
"""The logger for this module."""


class SRSender(Sender):
    def __init__(self, windowsize, *args, **kw):
        super().__init__(*args, **kw)
        self.windowsize = windowsize
        self.nextseqnum = 1
        self.window = []
        self.acked = {}
        self.incoming_messages = []
        # start the mini timer running
        self.start_timer(0)
        self.timeout_events = {}
        # maps sent packet to whether it has been acked
        #self.sent_packets = []
        #self.unsent_packets = []
        # a mapping from time (depending on granularity) to list of packets to
        # send at that time

    def from_layer5(self, message):
        if len(self.window) >= self.windowsize:
            self.incoming_messages.append(message)
        else:
            self.dispatch_packet(message)

    def schedule_timeout(self, timeout, packet):
        # TODO granularity here is one second, so we use int to determine
        # which interval the new time is in
        new_time = int(self.get_time() + self.timeout)
        if new_time not in self.timeout_events:
            self.timeout_events[new_time] = []
        self.timeout_events[new_time].append(packet)

    def index_of(self, seqnum):
        """Returns the index of the packet whose sequence number is `seqnum`
        in the current window, or raises a `ValueError` if no such packet
        exists.

        """
        return list(map(lambda p: p.seqnum, self.window)).index(seqnum)

    def from_layer3(self, packet):
        if self.is_corrupt(packet):
            return
        if self.acked[packet.acknum]:
            return
        try:
            index = self.index_of(packet.acknum)
        except ValueError:
            return
        # at this point we know the packet is in the window, not corrupt, and
        # has not already been acked
        acked_packet = self.window[index]
        self.received_at[packet.acknum] = self.get_time()
        self.acked[packet.acknum] = True
        self.remove_timers_for(acked_packet)
        while len(self.window) > 0 and self.acked[self.window[0].seqnum]:
            self.window.pop(0)
        while (len(self.window) < self.windowsize
               and len(self.incoming_messages) > 0):
            message = self.incoming_messages.pop(0)
            self.dispatch_packet(message)

    def dispatch_packet(self, message):
        packet = self.make_packet(self.nextseqnum, 0, message.data)
        self.to_layer3(packet)
        self.sent_at[packet.seqnum] = self.get_time()
        self.acked[packet.seqnum] = False
        self.schedule_timeout(self.timeout, packet)
        self.window.append(packet)
        self.nextseqnum += 1

    def remove_timers_for(self, packet):
        for packets in self.timeout_events.values():
            try:
                packets.remove(packet)
                return
            except ValueError:
                pass

    def timer_interrupt(self):
        current_time = int(self.get_time())
        if current_time in self.timeout_events:
            packets_to_send = self.timeout_events.pop(current_time)
            for packet in packets_to_send:
                self.to_layer3(packet)
                self.num_retransmitted += 1
                self.schedule_timeout(self.timeout, packet)
        self.start_timer(1)


class SRReceiver(Receiver):
    def __init__(self, windowsize, *args, **kw):
        super().__init__(*args, **kw)
        self.windowsize = windowsize
        self.received_packets = {}
        self.expected_seqnum = 1

    def from_layer3(self, packet):
        if self.is_corrupt(packet):
            return
        if packet.seqnum >= self.expected_seqnum + self.windowsize:
            return
        ack = self.make_packet(0, packet.seqnum, '')
        self.to_layer3(ack)
        if packet.seqnum >= self.expected_seqnum:
            self.received_packets[packet.seqnum] = packet
            while self.expected_seqnum in self.received_packets:
                old_packet = self.received_packets.pop(self.expected_seqnum)
                self.to_layer5(old_packet.data)
                self.expected_seqnum += 1
