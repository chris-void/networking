# CS655 routing simulation #

This is the experimental results report for the CS655 routing simulation

This file is written in the markup language "[Markdown][1]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
November 2011

[1]: http://daringfireball.net/projects/markdown

## Simulator design ##

I translated and re-implemented the provided simulation code from Java to
Python. It is now written in beautiful, modern, object-oriented Python, and is
easily extensible and testable. The `Node` class in the
`routing.protocols.bases` module contains the basic scheduling code. It
receives a reference to the scheduler object for the entire simulation, which
is an instance of Python's built-in `sched.scheduler` class (a lightweight
heap-based scheduler). It uses `sched.scheduler.enter` to schedule packet
arrival events on other nodes when the `to_layer2()` method is executed. It
also performs the sanity checks (including dropping packets sent to nodes which
are not neighbors of that node, etc.).

The `routing.protocols.distancevector` and `routing.protocols.pathvector`
provide implementations for the nodes in the distance vector and path vector
protocols, respectively. Each node is a subclass of
`routing.protocols.bases.Node`. In this way, new protocols can be easily added.

The `routing.simulation.Simulation` class encapsulates a single instance of the
simulation with a specific set of parameters, and the
`routing.simulation.runner` module provides a convenience function for running
a single instance of the simulation.

The `runonce.py` script performs a single run of the simulation.

## Correctness ##

The distance vector protocol sort of works, but I couldn't even get the path
vector protocol to run without errors. The pseudocode given in the paper does
not work as provided, was generally ambiguous, and was therefore insufficient
to construct a correct, running algorithm. I failed to figure out what the
authors intended. Please take a look at my code and let me know where the
problem is (you may need to look through the history in the Mercurial
repository to find some alternate versions of the code; I believe the current
one has some modifications of the pseudocode algorithm presented in the paper
which are attempts to fix their algorithm).

For tests of correctness, see the unit tests in the `tests` directory. To
ensure that all the tests pass, you can run the `run-tests.sh` script in this
directory. To check that, for example, scheduling an arrival works correctly,
run the following:

    python -m unittest \
      tests.test_protocols.test_bases.NodeTest.test_schedule_arrival

For more information, see the "Testing" section of `README.md`.

**Note**: some tests currently fail because they are not yet implemented.

## Experiments ##

The experiment simply runs the simulation and prints the results so that we can
examine the distance matrices and routing tables for correctness.

## Instructions for running the simulation ##

For instructions on running the simulation and for other general information
about the contents of this directory, see the `README.md` file.

## Output ##

Transcripts from example runs of the simulation with and without link changes
for the distance vector protocol can be found in the `results` directory.
