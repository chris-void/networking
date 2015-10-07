# CS655 error control simulation #

This is the experimental results report for the CS655 reliable data
transfer/error control simulation.

This file is written in the markup language "[Markdown][1]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
November 2011

[1]: http://daringfireball.net/projects/markdown

## Simulator design ##

I translated and re-implemented the provided simulation code from Java to
Python. It is now written in beautiful, modern, object-oriented Python, and is
easily extensible and testable. Most of the simulation code is in the
`simulation.endpoints.bases` module. The `Sender` class in that module receives
a reference to the scheduler object for the entire simulation, which is an
instance of Python's built-in `sched.scheduler` class (a lightweight heap-based
scheduler). It uses `sched.scheduler.enter` to schedule timer interrupt events
(when requested) and layer 5 message arrivals (randomly). The packet
transmission functionality, which includes corrupting and dropping packets and
scheduling the arrival of the packet on the other end of the link, is
controlled by the `simulation.links.UnidirectionalLink` class. Its subclass,
`simulation.links.UnreliableUnidirectionalLink`, corrupts and drops packets
with certain probabilities.

The `simulation.endpoints.alternatingbit`, `simulation.endpoints.gobackn`, and
`simulation.endpoints.selectiverepeat` provide implementations for the senders
and receivers of the alternating bit, go back N, and selective repeat
protocols, respectively. Each sender is a subclass of
`simulation.endpoints.bases.Sender` and each receiver is a subclass of
`simulation.endpoints.bases.Receiver`. In this way, new protocols can be easily
added.

The `simulation.simulation.Simulation` class encapsulates a single instance of
the simulation with a specific set of parameters, and the `simulation.runner`
module provides a convenience function for running and getting the statistics
from a single instance of the simulation.

The `experiments.py` iterates over all possible combination of input parameters
and outputs the results of running the simulation with those parameters.

## Correctness ##

For tests of correctness, see the unit tests in the `tests` directory. To
ensure that all the tests pass, you can run the `run-tests.sh` script in this
directory. To check that, for example, attempting to start a timer adds a new
timeout event, run the following:

    python -m unittest \
      tests.test_endpoints.test_bases.SenderTest.test_start_timer

For more information, see the "Testing" section of `README.md`.

**Note**: some tests currently fail because they are not yet implemented.

## Experiments and statistics collection ##

The experiment measures the average round-trip time of a packet (from the time
at which the sender first transmits it to the time at which the sender receives
the first ACK for it) as it depends on corruption probability of the link and
loss probability of the link, for both go back N and selective repeat
protocols.

For the go back N protocol, the time at which the packet is sent is recorded in
the `dispatch_packet` method of the `simulation.endpoints.gobackn.GBNSender`
class, the first time that a packet is sent. The time at which the packet is
received is recorded in the `from_layer3` method of the same class, when the
sender receives an ACK for that packet or a packet with a greater sequence
number in the window. These times are recorded in the same methods of the
corresponding classes in the selective repeat module.

In the experiment, the receiver responds to packets indefinitely, and the
sender sends messages as soon as they are generated (which is random but
depends on the average delay between message generation provided in the
constructor to the sender's class). The simulation stops when a specified
maximum number of messages have been generated, but not all of those messages
will necessarily have been acknowledged by the receiver, and they may not have
even been transmitted by the sender (due to finite window size and congestion).

We perform five independent trials of this simulation with maximum 1000
messages generated, an average delay of 40 time units between message
generation events, a window size of 8, and a retransmission timeout of 20. Our
final measured value is taken to be the arithmetic mean of the measured average
round-trip times of all packets sent (and acknowledged) during the simulation.

The retransmission timeout was chosen to be 20 because this twice the average
one-way propagation delay. The one-way propagation delay is given in the code
by the expression

    arrival_time = time_of_last_arrival + (9 * self.rand.next_double(2) + 1)

In this way, we retransmit if a packet has taken longer than its approximate
expected round-trip time to return.

## Instructions for running the simulation ##

For instructions on running the simulation and for other general information
about the contents of this directory, see the `README.md` file.

## Experiment environment ##

The experiments were run at approximately 19:48 on 7 November 2011 on
`orc.bu.edu` (maximizing utility of the many cores).

## Output and plots ##

Transcripts from example runs of the simulation with go back N and selective
repeat protocols can be found in the `results` directory.

Plots of mean round-trip time as it depends on corruption probability and loss
probability for each protocol can be found in the `results` directory. The
corresponding data which produced those plots can be found in the `data` file
in the same directory. In the plots of round-trip time, lower is better. The
time units are arbitrary.

The 90% confidence intervals shown for selective repeat, but not for go back N,
because the intervals are very large compared to the measured mean and
therefore make the plot very difficult to read.

## Interpretation of plots ##

In the plot of average packet round-trip time as it depends on corruption
probability and loss probability for each protocol, we can clearly see that at
each loss probability, round-trip time is directly proportional to corruption
probability, and at each corruption probability, round-trip time is directly
proportional to loss probability. For both protocols, round-trip time increases
as both loss and corruption increase.

However, go back N has more highly increasing average round-trip times (peak
around 700 time units for 0.5 corruption and 0.5 loss probability) compared to
selective repeat (peak around 200 time units with the same parameters). This is
expected: selective repeat is more efficient because it avoids putting packets
on the link if it doesn't need to, and this therefore clears up some of the
congestion seen in the go back N simulation. Of course, selective repeat has a
greater processing time and memory cost because it is slightly more complicated
to keep track of which packets have been sent but not acknowledged.

## Tradeoffs and extensions ##

In this simulation, we did not use sequence numbers which wrap around. It was
attempted but proved to be too complicated. This would save some space, as we
currently use lists allocated on the heap, and arbitrarily large integer
sequence numbers.

We could easily extend these protocols to have a handshake phase to initialize
a connection and a termination phase to close the connection. The constructor
for the `Sender` class might do this on instantiation, by sending an initial
packet and waiting for it to get acknowledged, like in TCP.
