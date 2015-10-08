# CS655 TCP socket echo server #

The report for the CS655 TCP socket echo server experiment.

This file is written in the markup language "[Markdown][1]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
October 2011

[1]: http://daringfireball.net/projects/markdown

## Server and client design ##

The server creates a socket on the port specified by the command-line
argument. It listens for connections, and on each connection attempts to handle
all incoming messages according to the protocol. The
`server.MeasurementProtocolHandler.handle` function repeatedly receives input
from the client request and acts upon it according to the protocol in the
assignment (either echoing back the received message or responding with an `OK`
or an `ERROR`).

The client creates a socket connection to the host and port specified by the
command-line arguments. It then sends the connection setup message, measurement
phase messages, and connection termination message to the server, in that
order. The client waits for an appropriate response after each message. If an
inappropriate response is received, an exception is raised.

## Correctness ##

For tests of correctness, see the unit tests in the `tests` directory. To
ensure that all the tests pass, you can run the `run-tests.sh` script in this
directory. To check that, for example, the server responds correctly for all
bad inputs in the measurement phase, run the following command:

    python -m unittest \
      tests.test_server.MeasurementProtocolHandlerTest.test_measurement

For more information, see the "Testing" section of `README.md`.

**Note**: it currently seems that there is some sort of bug preventing the
`run-tests.sh` script from running correctly, so run each of the test functions
individually as shown above.

## Experiments and statistics collection ##

This package performs two experiments. The first measures round-trip time of a
message as it depends on message size, and the second measures throughput of a
path as it depends on message size. We also examine how these values change
depending on propagation delay (which is simulated by a delay at the server).

In the former experiment, the client sends messages of size 1, 100, 200, 400,
800, and 1000 bytes and in the latter experiment, the client sends messages of
size 1, 2, 4, 8, 16, and 32 kibibytes (2^10 bytes). The round-trip time is the
difference between the time at which the client sends the bytes and the time at
which the client receives the echoed response from the server. The throughput
is the message size divided by the round-trip time.

The time at which the client sends a message is recorded immediately before
calling the `socket.send()` function, and the time at which the client receives
a message is recorded immediately following the call to `socket.recv()` (at
which point the entire echoed message has been received from the server and
made available to the client program in memory).

The client sends ten messages of each size, and the round-trip time or
throughput for that message size for the experiment is recorded as the average
over those ten recorded values. We perform five independent trials of this
experiment, to get five mean measurements, and the final value is taken as the
average of those five mean measurements.

## Instructions for running the client and server ##

For instructions on running the client and the server and for other general
information about the contents of this directory, see the `README.md` file.

## Experiment environment ##

The experiments were run at approximately 16:00 on 12 October 2011, with the
server running on host grubnick.bu.edu and port 10101, and the client running
on host csa2.bu.edu, both Linux hosts with wired ethernet connections.

## Plots ##

Plots of mean round-trip time as it depends on message size and mean throughput
as it depends on message size for three different values of server delay can be
found in the `plots` directory. The corresponding data which produced those
plots can be found in the `data` file in the same directory. In the plots of
round-trip time, lower is better. In the plots of throughput, higher is better.

## Interpretation of plots ##

As message size increases so does round-trip time in a nearly linear
manner. This confirms our expectation that a longer message takes longer to
send and receive because there are more bits over a channel with fixed physical
limitations.

As message size increases so does throughput, quickly at first but eventually
flattening out. (The introduction of server delay diminishes this effect
because the delay begins to dominate the sending and receiving time.) This
confirms our expectation that as the length of a message increases to infinity,
this situation begins to approximate the actual throughput of the channel
(since we are putting an infinite stream of bits on the channel and measuring
how long it takes to receive them).
