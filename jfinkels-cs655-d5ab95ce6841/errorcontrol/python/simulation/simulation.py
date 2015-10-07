# simulation.py - encapsulation for an instance of the simulation
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides a class which encapsulates a single trial of the simulation with a
particular set of parameters.

"""
import io
import logging
import sched
import sys

from .endpoints.alternatingbit import ABSender
from .endpoints.alternatingbit import ABReceiver
from .endpoints.gobackn import GBNSender
from .endpoints.gobackn import GBNReceiver
from .endpoints.selectiverepeat import SRSender
from .endpoints.selectiverepeat import SRReceiver
from .links import UnreliableUnidirectionalLink as Link
from .random import OSIRandom

LOG_FORMAT = '[%(module)s %(levelname)s] %(message)s'
"""The formatting string for logged messages."""
TO_DEBUG_LEVEL = {-1: logging.ERROR, 0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG,
                  3: logging.DEBUG, 4: logging.DEBUG}
"""Mapping from `trace` simulation parameter to logging level."""


class Timer(object):
    """An object which maintains a current time and which can be delayed."""

    def __init__(self, initial_time=0):
        """Sets the time to initially be `initial_time`."""
        self.time = initial_time

    def delay(self, delay_time):
        """Delays the current simulation by the specified delay."""
        self.time += delay_time

    def get_time(self):
        """Returns the current simulation time."""
        return self.time


class Simulation(Timer):
    """Represents a single instance of the simulation with a specified set of
    parameters.

    After running this simulation with the `run()` function, the transcript of
    messages received by layer 5 on the receiver side can be retrieved by
    accessing the `output` attribute. The time of termination can be retrieved
    by calling the `get_time()` function.

    """

    def __init__(self, protocol='AB', num_messages=25, loss_probability=0.2,
                 corruption_probability=0.2, avg_delay=40, trace=2, seed=None,
                 windowsize=8, timeout=20):
        """Initializes the scheduler, the endpoints, the links, etc. necessary
        for the simulation.

        `protocol` must be one of `'AB'`, `'GBN'`, or `'SR'`, for "alternating
        bit", "go back N", and "selective repeat", respectively.

        """
        super().__init__()
        logging.basicConfig(format=LOG_FORMAT, level=TO_DEBUG_LEVEL[trace])
        random = OSIRandom(seed)
        self.scheduler = sched.scheduler(self.get_time, self.delay)
        self.outfile = io.StringIO()
        if protocol == 'AB':
            self.sender = ABSender(self.scheduler, timeout, num_messages,
                                   avg_delay, random)
            self.receiver = ABReceiver(self.scheduler, self.outfile)
        elif protocol == 'GBN':
            self.sender = GBNSender(windowsize, self.scheduler, timeout,
                                    num_messages, avg_delay, random)
            self.receiver = GBNReceiver(self.scheduler, self.outfile)
        elif protocol == 'SR':
            self.sender = SRSender(windowsize, self.scheduler, timeout,
                                   num_messages, avg_delay, random)
            self.receiver = SRReceiver(windowsize, self.scheduler,
                                       self.outfile)
        else:
            raise ValueError("protocol must be one of 'AB', 'GBN', or 'SR'")
        self.sender_to_receiver = Link(self.scheduler, self.receiver,
                                       loss_probability,
                                       corruption_probability, random)
        self.receiver_to_sender = Link(self.scheduler, self.sender,
                                       loss_probability,
                                       corruption_probability, random)
        self.sender.set_link(self.sender_to_receiver)
        self.receiver.set_link(self.receiver_to_sender)

    def run(self):
        """Runs the simulation."""
        self.sender.generate_next_arrival()
        self.scheduler.run()
        self.output = self.outfile.getvalue()
        self.outfile.close()

    def throughput(self):
        return self.receiver.num_received / self.time

    def goodput(self):
        return (len(self.output.split()) / self.time)

    def round_trip_times(self):
        result = []
        for packet_num in self.sender.received_at:
            rcvd_at = self.sender.received_at[packet_num]
            sent_at = self.sender.sent_at[packet_num]
            result.append(rcvd_at - sent_at)
        return result

    def num_corrupt(self):
        return self.sender_to_receiver.num_corrupt \
            + self.receiver_to_sender.num_corrupt

    def num_sent(self):
        return self.sender.num_sent

    def num_lost(self):
        return self.sender_to_receiver.num_lost \
            + self.receiver_to_sender.num_lost

    def num_retransmitted(self):
        return self.sender.num_retransmitted
