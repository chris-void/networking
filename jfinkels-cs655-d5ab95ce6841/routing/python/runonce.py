# runonce.py - runs a parameterized instance of the simulation
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Runs a single instance of the simulation with a particular set of
parameters.

This module can be run from the command-line, like this::

    python3 runonce.py

There are a bunch of command-line parameters for this program. You can view
them by running

    python3 runonce.py -h

"""
import argparse

from routing.runner import run_parameterized_simulation

DESCRIPTION = """
Runs the routing simulation.
""".strip()

argparser = argparse.ArgumentParser(description=DESCRIPTION)
argparser.add_argument('-v', '--trace', type=int, choices=range(4), default=0,
                       help='the level (verbosity) of debug messages to log')
argparser.add_argument('-s', '--seed', type=int, default=0,
                       help='the seed to the random number generator')
argparser.add_argument('-p', '--protocol', choices=('DV', 'PV'),
                       default='DV', help='the routing protocol')
argparser.add_argument('-l', '--link-changes', action='store_true',
                       help=('whether the cost of a link will change during'
                             ' the simulation'))

result = run_parameterized_simulation(**vars(argparser.parse_args()))
#print('*** results')
# ...
