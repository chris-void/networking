# runonce.py - runs a parameterized instance of the simulation
#
# CS655 error control assignment
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

from simulation.runner import run_parameterized_simulation

DESCRIPTION = """
Runs the error control simulation.
""".strip()

argparser = argparse.ArgumentParser(description=DESCRIPTION)
argparser.add_argument('-n', '--num-messages', type=int, default=25,
                       help='the maximum number of messages to simulate')
argparser.add_argument('-l', '--loss-probability', type=float, default=0.2,
                       help=('the probability of losing a sent packet (between'
                             ' 0 and 1, inclusive)'))
argparser.add_argument('-c', '--corruption-probability', type=float,
                       default=0.2, help=('the probability of corrupting a'
                                         ' sent packet (between 0 and 1,'
                                         ' inclusive)'))
argparser.add_argument('-d', '--avg-delay', type=int, default=40,
                       help=('average delay time between messages from layer 5'
                             ' in the sender'))
argparser.add_argument('-w', '--windowsize', type=int, default=8,
                       help='the size of the packet window')
argparser.add_argument('-t', '--timeout', type=float, default=20.,
                       help='retransmission timeout')
argparser.add_argument('-v', '--trace', type=int, choices=range(4), default=0,
                       help='the level (verbosity) of debug messages to log')
argparser.add_argument('-s', '--seed', type=int, default=0,
                       help='the seed to the random number generator')
argparser.add_argument('-p', '--protocol', choices=('AB', 'GBN', 'SR'),
                       default='AB', help='the sender and receiver protocol')

result = run_parameterized_simulation(**vars(argparser.parse_args()))
print('*** results')
print('throughput:', result.throughput)
print('goodput:', result.goodput)
print('mean RTT:', result.mean_rtt)
print('number of unique sent packets:', result.num_sent)
print('number of retransmitted packets:', result.num_retransmitted)
print('number of corrupted packets:', result.num_corrupt)
print('number of lost packets:', result.num_lost)
