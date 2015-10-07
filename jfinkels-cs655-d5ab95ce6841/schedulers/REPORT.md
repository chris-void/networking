# CS655 scheduler simulation report #

The report for the CS655 packet traffic simulation.

This file is written in the markup language "[Markdown][1]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
October 2011

[1]: http://daringfireball.net/projects/markdown

## Design and statistics collection documentation ##

For design and statistics collection documentation, see the `DESIGN.md` file in
this directory.

## Instructions for running the simulation ##

For instructions on running the simulation and for other general information
about the contents of this directory, see the `README.md` file.

## Correctness ##

For tests of correctness, see the unit tests in the `tests` directory. For
example, the `tests.test_runner.MiscTest` test case tests that for two traffic
sources under any scheduler, the measured throughputs are proportional to the
generation rates. There are also tests in `tests.test_runner` that, for
example, for a single traffic source and a FIFO scheduler, the measured
throughput matches the expected throughput.

To make sure that all the tests pass, you can run the `run-tests.sh` script in
this directory. For more information, see the "Testing" section of `README.md`.

## Plots ##

Plots of mean latency as it depends on total offered load and ratio of measured
throughput to expected throughput as it depends on total offered load for each
traffic source and each scheduler can be found in the `plots` directory. The
corresponding data which produced those plots can be found in the `data` file
in the same directory. In the plots of latency, lower is better. In the plots
of throughput, higher is better.

Note that in the plots for latencies, the 90% confidence intervals are not
shown because they seem to be orders of magnitude greater than the plotted
values. In the plots for throughput ratio, the 90% confidence intervals are
plotted, but too small to be noticed.

## Interpretation of plots ##

### Telnet sources ###

Observing the plots, we see that for sources 0 through 5, which are telnet
sources, latency is highest for the round-robin scheduler and lowest for the
FIFO scheduler. Latency is slightly higher for the deficit round-robin
scheduler than for the FIFO scheduler. The latency increases (quickly at first,
then slowing) for all schedulers as total offered load increases.

The round-robin scheduler may perform relatively poorly for telnet sources
because such sources create many small packets which will wait in their
respective queues for a long time before servicing, whereas a source creating
fewer large packets will wait for a relatively shorter time since there are
fewer packets in that queue. In a FIFO scheme, creating many small packets
ensures that they will be serviced quickly if they arrive before other larger
packets. Deficit round-robin is better than round-robin here because it solves
the problem of servicing only one packet per queue per round, but slightly
worse than FIFO because the quantum size is fixed and therefore will still
leave some packets waiting in their respective queues.

Throughput ratios seem to be indistinguishable for source 0 through 5 (the
telnet sources) with respect to scheduler type. Throughput ratio decreases as
total offered load increases, as expected. Greater congestion means it takes
relatively longer to get all bits processed.

### FTP sources ###

For sources 6 through 10, which are FTP sources, latency is lowest for the
round-robin scheduler and highest for the deficit round-robin
scheduler. Latency is slightly lower for the FIFO scheduler than for the
deficit round-robin scheduler. As with the telnet sources, the latency
increases (quickly at first, then slowing) for all schedulers as total offered
load increases.

The round-robin scheduler may perform relatively well for FTP sources because
they such sources create a small number of large packets which will not wait
very long in their respective queues (since round-robin dequeues one packet
from each user's queue per round). In a FIFO scheme, the few large packets will
have to wait for the many small packets to be dequeued before being
serviced. Deficit round-robin is slightly worse than FIFO here because it
allows many small packets to be dequeued from each of the other queues before
servicing the few large packets.

The round-robin scheduler has a higher throughput ratio than the other two
scheduler types. The throughput ratios for the FIFO and deficit round-robin
schedulers are indistinguishable. The throughput may be relatively higher for
the round-robin scheduler because of the same reasons stated in the previous
paragraph justifying its low latency. The throughput ratio decreases as total
offered load increases, as expected.

### Rogue source ###

For the rogue source, latency is highest for the FIFO scheduler and lowest for
the round-robin scheduler. Latency is slightly higher for the deficit
round-robin scheduler than for the round-robin scheduler. For the FIFO
scheduler, latency is gradually increasing as the total offered load increases
to about 1.0, and after that it is somewhat stable. This is because as the
total offered load of the other traffic sources increases, the waiting time in
the queue for the packets generated by the rogue source increases. For the
round-robin and deficit round-robin scheduler, latency is decreasing (quickly
at first, then slowing) as total offered load increases. This is because the
offered load of the rogue source does not depend on the total offered load, so
the relative waiting time decreases.

The FIFO scheduler may perform poorly for the rogue source because its packets
must wait for all other packets in the queue to be dequeued. The round-robin
scheduler may perform well because the waiting time for the rogue source
packets is relatively smaller since one packet from each queue is removed on
each round. The deficit round-robin scheduler may perform worse than the
round-robin scheduler since it allows multiple packets to be dequeued from each
of the other queues before servicing the rogue packets.

Throughput ratio is highest for round-robin and lowest for FIFO, both initially
decreasing quickly but eventually leveling off. Throughput ratio for deficit
round-robin is initially decresing, then nearly uniform with respect to total
offered load. These shapes are as expected: since the offered load of the rogue
source is independent of the total offered load, when the total offered load is
small the other traffic sources do not produce as much traffic so the packets
generated by the rogue source make it through the pipeline relatively
quickly. When the total offered load is large, the other traffic sources have
more packets in the queues, so the throughput for the rogue source is not as
high.

Throughput ratio may be highest with round-robin since it uniformly chooses one
of the rogue source's packets on each round, only waiting for one packet to be
removed from each of the other queues. Throughput ratio may be worst with FIFO
because as the other traffic sources enqueue more packets, the rogue source's
packets must wait longer. Deficit round-robin performs somewhere in the middle
for the reasons stated in the previous justifications.

## Time and space complexity ##

If the number of users which provide packets to a scheduler is *n*, then
dequeuing from a round-robin scheduler has *O(1)* time complexity (because we
just store and increment a pointer to the next user's queue) and *O(n)* space
complexity (because we store one queue for each user; assume the number of
packets is fixed and therefore does not affect the space complexity). For a
fixed quantum size, dequeuing from the deficit round-robin scheduler also has
*O(1)* time complexity (because although we need to check if the next packet in
the current user's queue can be dequeued, the check is constant time because
the size of the quantum is fixed) and *O(n)* space complexity (for the *n*
queues; there is additional space used by the [fixed number of] packets in the
queues and the *n* deficit counters, but these are absorbed by the big-O).

## Is deficit round-robin worth it? ##

According to this data, deficit round-robin seems to be a fair compromise
between naive round-robin and FIFO. In an environment in which there are
sources generating many small packets and sources generating few large packets,
it services small packets relatively quickly. It does not seem to perform well
for those few large packets though, compared to naive round-robin, since
round-robin simply chooses one packet from each queue, regardless of
size. Whether to use deficit round-robin depends on what type of traffic you
value more highly and in what environment it will be running.
