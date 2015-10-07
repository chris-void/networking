# bases.py - abstract base classes for senders and receivers for reliable data transfer
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides the abstract base classes for reliable data transfer senders and
receivers.

"""
import logging
from string import ascii_lowercase as LETTERS

from ..datacontainers import MAX_DATA_SIZE
from ..datacontainers import Message
from ..datacontainers import Packet

logger = logging.getLogger(__name__)
"""The logger for this module."""


class Endpoint(object):
    """A traffic source or traffic sink which can send along and receive
    packets from layer 3.

    Client code must call the `set_link` function to set a `Link` object.

    Subclasses must override the function `from_layer3`.

    """

    def __init__(self, scheduler):
        """Instantiates this traffic endpoint with the specified unreliable
        link and scheduler.

        """
        self.link = None
        self.scheduler = scheduler
        self.num_sent = 0
        self.num_received = 0
        self.num_corrupt = 0

    def is_corrupt(self, packet):
        """Returns `True` if and only if the specified packet is corrupt (that
        is, the checksum provided in the packet does not match the checksum
        computed from its sequence number, ACK number, and message data.

        """
        seqnum = packet.seqnum
        acknum = packet.acknum
        data = packet.data
        return packet.checksum != self.checksum(seqnum, acknum, data)

    def get_time(self):
        """Returns the current simulation time."""
        return self.scheduler.timefunc()

    def checksum(self, seqnum, acknum, message_data):
        """Returns the sum of `seqnum`, `acknum`, and each of the ordinals of
        the characters in `message_data`.

        """
        return seqnum + acknum + sum(ord(c) for c in message_data)

    def make_packet(self, seqnum, acknum, message_data):
        """Returns a new packet with the specified header info and data."""
        checksum = self.checksum(seqnum, acknum, message_data)
        return Packet(seqnum, acknum, checksum, message_data)

    def from_layer3(self, packet):
        """Receives a packet (an instance of the `Packet` class) from layer 3.

        The packet may be corrupted, a duplicate, or out of order.

        Subclasses must override this function.

        """
        pass

    def _from_layer3(self, packet):
        """Wrapper around the `from_layer3()` function which increments the
        total number of messages received.

        """
        self.num_received += 1
        self.from_layer3(packet)

    def set_link(self, link):
        """Sets the link along which packets can be sent.

        This function must be called immediately after instantiation, before
        any other function can be called.

        """
        self.link = link

    def to_layer3(self, packet):
        """Sends the specified packet along the unreliable link."""
        self.link.send(packet)


class Sender(Endpoint):
    """A traffic source which transmits messages from layer 5 over the network
    as packets to the receiver.

    Subclasses must override the `from_layer5` function and the
    `timer_interrupt` function, as well as the `Endpoint.from_layer3`.

    This class terminates the simulation when a maximum number of messages
    have been sent.

    """

    def __init__(self, scheduler, retransmission_timeout, max_messages,
                 avg_delay, random_number_generator):
        """Initialize this sender.

        `scheduler` is the `sched.scheduler` on which to schedule message
        generation and packet arrival events.

        `retransmission_timeout` is the time for the countdown timer which is
        reset each time a packet is sent.

        `max_messages` is the maximum number of messages to send. After this
        many messages have been received from layer 5 and sent out as packets,
        the simulation halts.

        `avg_delay` is the average delay between messages generated from layer
        5.

        `random_number_generator` is the instance of the pseudo-random number
        generator used throughout the simulation.

        """
        super().__init__(scheduler)
        self.timeout = retransmission_timeout
        self.max_messages = max_messages
        self.avg_message_delay = avg_delay
        # TODO should we just create a singleton instance in the random module?
        self.rand = random_number_generator
        self.num_retransmitted = 0
        self.waiting_packets = []
        # for measuring round-trip times
        self.sent_at = {}
        self.received_at = {}

        self._current_timer_event = None

    def _from_layer5(self, message):
        """Wrapper around the `from_layer5` function which generates a new
        arrival event after executing `from_layer5`.

        This function increments the counter for the number of messages sent,
        `num_sent`.

        This function should be the action in the event scheduled by the
        `generate_next_arrival` function when simulating a call from layer 5.

        """
        self.from_layer5(message)
        self.num_sent += 1
        if self.num_sent < self.max_messages:
            self.generate_next_arrival()
        else:
            # !!! WARNING !!!
            # Do not try this at home! Performing black magic on this instance
            # of sched.scheduler to clear the event queue to immediately halt
            # the simulation.
            logger.debug('Sender: Clearing the events in the scheduler queue.')
            for event in list(self.scheduler.queue):
                self.scheduler.cancel(event)

    def from_layer5(self, message):
        """Takes the specified message (an instance of the `Message` class)
        from layer 5 and puts a packet containing the content of the message
        on the network, destined for the receiver.

        This function does not increment the counter for the number of
        messages sent, `num_sent`.

        Subclasses must override this function. Classes which override this
        function should, in their implementation, call the `to_layer3`
        function when they have encapsulated the data from `message` into a
        `Packet` object.

        """
        pass

    def generate_next_arrival(self):
        """Schedules a new random message coming from layer 5 on this sender
        at a randomly chosen time in the future.

        Returns a handle for the event which was added.

        """
        delay = 2 * self.avg_message_delay * self.rand.next_double(0)
        message = Message(LETTERS[self.num_sent % 26] * MAX_DATA_SIZE)
        return self.scheduler.enter(delay, 1, self._from_layer5, (message, ))

    def start_timer(self, increment):
        """Starts the countdown timer from `increment` by scheduling a timer
        interrupt event to occur at `increment` timesteps from the current.

        If there is already a scheduled timer interrupt event, no new event is
        scheduled. Otherwise, a new event is scheduled and a handle for that
        event is returned.

        """
        logger.debug('start_timer(): starting timer at {}'
                      .format(self.scheduler.timefunc()))
        if self._current_timer_event is None:
            self._current_timer_event = self.scheduler.enter(increment, 1, self._timer_interrupt, ())
            return self._current_timer_event


    def stop_timer(self):
        """Cancels any countdown timer events in the event queue."""
        logger.debug('stop_timer(): stopping timer at {}'
                     .format(self.scheduler.timefunc()))
        if self._current_timer_event is not None:
            self.scheduler.cancel(self._current_timer_event)
            self._current_timer_event = None

    def _timer_interrupt(self):
        self._current_timer_event = None
        self.timer_interrupt()

    def timer_interrupt(self):
        """This function is called when this sender's timeout has expired.

        Subclasses must override this function.

        """
        pass


class Receiver(Endpoint):
    """A traffic sink which receives messages from a `Sender` and responds
    with ACK packets.

    Subclasses must override and implement the `Endpoint.from_layer3` function.

    """

    def __init__(self, scheduler, outfile):
        """Initializes this receiver with the specified link along which ACK
        packets will be sent, scheduler for scheduler packet arrival events on
        the destination, and an open file-like object `outfile` to which to
        write received messages from the sender.

        """
        super().__init__(scheduler)
        self.outfile = outfile

    def to_layer5(self, data):
        """Writes the data from the response packets received from the
        receiver to a file, one line per message received.

        """
        self.outfile.write(data + '\n')
