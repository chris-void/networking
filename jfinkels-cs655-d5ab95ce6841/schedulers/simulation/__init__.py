# __init__.py - file marking this directory as a Python package
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""This package provides the schedulers, sinks, sources, and analysis tools
required for the schedulers assignment.

When this package is run as a main module, it will run the simulation. To run
this as a main module, run the following command in the directory above this
one::

    python simulation

There are some required command-line arguments. To view the help message which
describes the arguments, run the command::

    python simulation --help

Besides the __main__ module, which runs the simulation, this package contains
the following modules::

* analysis - tools for statistical analysis after running the simulation
* endpoints - the classes which produce and consume packets via the schedulers
* runner - provides convenience functions for running a simulation with a
  specific set of parameters and getting the statistics for that simulation
* schedulers - contains the implementations of the FIFO, round-robin, and
  deficit round-robin schedulers

The discrete event simulation is handled by the SimPy library. Each endpoint in
the `endpoints` module is a SimPy `Process`, which represents an active entity
running in a discrete event simulation. The traffic sources and sinks in that
module schedule packet generation and consumption events, and SimPy handles the
simulation bookkeeping.

"""
