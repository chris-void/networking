# links.py - the link along which data can be transmitted
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides reliable and unreliable links along which data can be sent."""
import copy
import heapq
import logging

logger = logging.getLogger(__name__)
"""The logger for this module."""


class Link(object):
    """A base class for any type of link along which data can be sent among
    hosts.

    """
    pass


class UnidirectionalLink(Link):
    """A base class for a unidirectional link."""

    def __init__(self, scheduler, destination, random_number_generator):
        """Instantiates this link with the specified scheduler, destination
        (an `Endpoint` object), and random number generator.

        """
        self.scheduler = scheduler
        self.destination = destination
        self.rand = random_number_generator

    def send(self, packet):
        """Sends the specified packet to the destination along this link
        without corruption or loss.

        Does not perform a deep copy of the provided packet, so the `Packet`
        object which arrives on the destination is the same instance of
        `Packet` provided as input to this function.

        """
        # WARNING! BLACK MAGIC! for the sake of optimization
        latest_events = list(filter(lambda e: e.action == self.destination.from_layer3, heapq.nlargest(2, self.scheduler._queue)))
        if len(latest_events) == 0:
            arrival_time = self.scheduler.timefunc()
        else:
            arrival_time = latest_events[0].time
        arrival_time += 9 * self.rand.next_double(2) + 1
        # schedule the arrival of this packet from layer 3 on the destination
        self.scheduler.enterabs(arrival_time, 1,
                                self.destination._from_layer3, (packet, ))


class UnreliableUnidirectionalLink(UnidirectionalLink):
    """An unreliable link (which may corrupt or drop packets) to a single
    destination.

    This class records the number of packets lost and the number of packets
    corrupted, but does not record the number of packets sent on this link.

    """

    def __init__(self, scheduler, destination, loss_probability,
                 corruption_probability, random_number_generator):
        """Instantiates this link with the specified event scheduler and
        destination host.

        """
        super().__init__(scheduler, destination, random_number_generator)
        self.loss_probability = loss_probability
        self.corruption_probability = corruption_probability
        self.num_lost = 0
        self.num_corrupt = 0

    def send(self, packet):
        """Sends the specified packet along this unreliable link to the
        destination specified in the constructor of this class, applying any
        loss or corruption that may occur on the link.

        Performs a deep copy of the provided packet, so the `Packet` object
        which arrives on the destination is a new instance of `Packet` with
        instance fields having the same values as the provided packet. Hence
        any corruption occurs on the copy, not on the input instance.

        """
        packet = copy.deepcopy(packet)
        logger.debug('send(): {}'.format(packet))
        # drop the packet with some probability
        if self.rand.next_double(1) < self.loss_probability:
            self.num_lost += 1
            logger.warn('send(): packet being lost')
            return
        # corrupt the packet with some probability
        if self.rand.next_double(3) < self.corruption_probability:
            self.num_corrupt += 1
            logger.warn('send(): packet being corrupted')
            x = self.rand.next_double(4)
            if x < 0.75:
                packet.data = '?' + packet.data[1:]
            elif x < 0.875:
                packet.seqnum = 999999
            else:
                packet.acknum = 999999
            logger.warn('  new packet: {}'.format(packet))
        # after loss or corruption, simply send the packet to the destination
        super().send(packet)
