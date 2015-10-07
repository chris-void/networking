# endpoints.py - the sources and sinks for packet traffic in the simulation
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Provides sources and sinks for packet traffic in the simulation.

The two main classes which this module provides are `TrafficSource` and
`TrafficSink`, both subclasses of the SimPy `Process` class. The
`TrafficSource` class, when started in a SimPy simulation, generates packets at
a given average rate and enqueues them on the packet switch (which is modeled
by one of the schedulers). The `TrafficSink` class, when started in a SimPy
simulation, dequeues packets at a certain rate from the packet switch (if there
are packets to dequeue).

The `TrafficManager` class tracks the number of packets generated by the
traffic sources which it manages.

"""
# TODO use a SimPy `Store` object as the packet switch device?

import logging
import random

from SimPy.Simulation import hold
from SimPy.Simulation import Process
from SimPy.Simulation import Monitor
from SimPy.Simulation import waituntil

from schedulers import Item

OUTPUT_LINK_RATE = 1.0
"""The rate at which the output link outputs packets (in bits per second)."""
logger = logging.getLogger(__name__)
"""The logger for this module."""


class TrafficManager(object):
    """A manager for multiple traffic sources connected to a traffic sink.

    This class maintains a count of the number of packets generated by all
    traffic sources which it manages.

    """

    def __init__(self, max_packets=100000):
        """Initializes the number of packets generated to 0, and stores the
        maximum number of packets which will be generated by sources for which
        this object is the manager.

        """
        self.num_packets_generated = 0
        self.max_packets = max_packets

    def max_packets_reached(self):
        """Returns `True` if and only if the number of packets which have been
        generated by the traffic sources for which this object is a manager is
        greater than or equal to the maximum number of packets specified in the
        constructor of this class.

        """
        return self.num_packets_generated >= self.max_packets


class TrafficEndpoint(Process):
    """A base class for a source or sink of packet traffic.

    This class extends `SimPy.Process`, which represents an active object in
    the simulation.

    Functions in classes which inherit from this base class may call the `log`
    function to log messages.

    """
    def __init__(self, scheduler, manager, *args, **kw):
        """Instantiates this endpoint with access to the specified `scheduler`,
        on which packets are dequeued if this endpoint is a sink, or on which
        packets are enqueued if this endpoint is a source.

        Passes on the positional and keyword arguments to the constructor of
        the superclass.

        `manager` is the `TrafficManager` object which manages this traffic
        source and the sink to which it is directed. This is necessary because
        the `TrafficManager` maintains a count of how many packets have been
        generated by all traffic sources under its management. The simulation
        ends after the maximum number of packets (as specified by the manager)
        have been generated.

        """
        super(TrafficEndpoint, self).__init__(*args, **kw)
        self.scheduler = scheduler
        self.manager = manager

    def log(self, message, level=logging.DEBUG):
        """Log the specified `message` at the given logging `level`, along with
        the current simulation time.

        Subclasses should use this function, instead of explicitly calling
        `logging.debug` to log debug messages.

        """
        logger.log(level, '{0}: {1}'.format(self.sim.now(), message))


class TrafficSource(TrafficEndpoint):
    """A source of packet traffic, which generates packets of various sizes at
    a specified rate.

    Each generated packet is enqueued on the scheduler specified in the
    constructor of this class.

    """
    def __init__(self, scheduler, source_id, avg_packet_size, generation_rate,
                 manager, random_number_generator=random, *args, **kw):
        """Instantiates this traffic source which creates packets.

        `scheduler` is the object on which generated packets will be enqueued.

        The `source_id` is the unique identifying integer of this source. This
        is used by the packet switch to identify the source of the incoming
        packets.

        The `avg_packet_size` is the arithmetic mean of packet sizes (in bits)
        created by this traffic source.

        The `generation_rate` is the rate (in bits per second) at which data is
        created by this source. Once the generated data reaches the expected
        packet size, the packet is sent to the packet switch.

        `random` is the random number generator for this simulation. Must have
        a `expovariate` function.

        Passes on the positional and keyword arguments to the constructor of
        the superclass.

        """
        super(TrafficSource, self).__init__(scheduler, manager, *args, **kw)
        self.source_id = source_id
        self.avg_packet_size = avg_packet_size
        self.generation_rate = generation_rate
        self.random = random_number_generator
        self.bits_generated = 0
        self.first_arrival_time = None

    def ACTIONS(self):
        """Creates and enqueues a packet on the scheduler.

        The length of the packet in bits is chosen at random from the
        exponential distribution with the mean specified in the constructor.

        This function loops continuously, waiting until the correct number of
        bits to create a packet has accumulated (by using the `yield hold`
        SimPy action) and then enqueuing the packet on the scheduler.

        Post-condition: the `arrival_time` attribute of the generated item is
        set to the time at which it arrives at the scheduler.

        """
        self.log('source {0} entering ACTIONS()'.format(self.source_id))
        while True:
            # generate a length in bits chosen from the exponential
            # distribution with mean `avg_packet_size`
            one_over_lambda = 1.0 / self.avg_packet_size
            packet_size = int(self.random.expovariate(one_over_lambda))
            # TODO allow packets of length 0?
            length = max(0, int(packet_size))
            item = Item(self.source_id, length)
            self.log('source {0} generating item {1}'.format(self.source_id,
                                                             item))
            # the time required to accumulate all the bits into a packet
            time = item.length / self.generation_rate
            # wait until the bits of a full packet have been generated
            self.log('source {0} holding for {1}'.format(self.source_id, time))
            yield hold, self, time
            # if too many packets have been created in the time since we
            # started holding, don't create anymore
            if self.manager.max_packets_reached():
                break
            self.log('source {0} enqueuing item {1}'.format(self.source_id,
                                                            item))
            self.scheduler.enqueue(item)
            self.bits_generated += item.length
            item.arrival_time = self.sim.now()
            if self.first_arrival_time is None:
                self.first_arrival_time = item.arrival_time
            self.manager.num_packets_generated += 1

        def __str__(self):
            """Returns the string representation of this traffic source."""
            return '<TrafficSource {0}>'.format(self.source_id)


class TrafficSink(TrafficEndpoint):
    """The object which receives packets dequeued from the scheduler."""
    def __init__(self, scheduler, manager, *args, **kw):
        """Creates the traffic sink with access to the specified scheduler.

        Passes on the positional and keyword arguments to the constructor of
        the superclass.

        """
        super(TrafficSink, self).__init__(scheduler, manager, *args, **kw)
        self.dequeued_items = []
        self.time_of_last_transmission = {}
        self.latency_monitors = {}
        self.log('creating traffic sink')

    def _scheduler_not_empty(self):
        """Returns `True` if and only if the scheduler has a packet to dequeue.

        """
        return len(self.scheduler) > 0

    def ACTIONS(self):
        """Dequeues packets from the scheduler specified in the constructor.

        This function only dequeues packets in the scheduler if they exist and
        the output link rate has allowed removing all the bits in the
        packet. If no packets exist in the queue, this function will do nothing
        until there are packets. If there are packets to dequeue, this function
        waits for the appropriate amount of time to process the packet, then
        dequeues the packet from the scheduler's queue. The time waited depends
        on the length of the packet and the output link rate.

        """
        while True:
            self.log('***start loop in TrafficSink.ACTIONS***')
            self.log('length of scheduler {0}'.format(len(self.scheduler)))
            self.log('total packets {0}'
                     .format(self.manager.num_packets_generated))
            if len(self.scheduler) == 0:
                if self.manager.max_packets_reached():
                    self.log('max packets reached!')
                    break
                self.log('waiting until not empty...')
                yield waituntil, self, self._scheduler_not_empty
            item = self.scheduler.dequeue()
            if item is None:
                self.log('no item dequeued probably too small for quantum')
                self.log('skipping to next round')
                continue
            self.log('starting to process packet {0}'.format(item))
            item.first_processed_time = self.sim.now()
            if item.owner not in self.latency_monitors:
                self.latency_monitors[item.owner] = Monitor(sim=self.sim)
                # TODO figure out when the transient state ends/the steady
                # state begins and use the following line to start
                # collecting data at a specific time
                #self.latency_monitors[item.owner].startCollection()
            # the arrival time is set by the traffic source
            latency = item.first_processed_time - item.arrival_time
            self.latency_monitors[item.owner].observe(latency)
            # wait for the bits of the packet to be processed
            # NOTE the dequeue should really come after this line, but this is
            # easier
            self.log('holding for {0}'.format(item.length))
            yield hold, self, item.length / OUTPUT_LINK_RATE
            # need to check for None because if the scheduler is DRR, the
            # peek() may have shown an item, but there may not be a large
            # enough quantum to dequeue its full length
            # TODO this will be expensive in space; is this necessary?
            self.dequeued_items.append(item)
            self.time_of_last_transmission[item.owner] = self.sim.now()
            self.log('dequeued and processed {0}'.format(item))
