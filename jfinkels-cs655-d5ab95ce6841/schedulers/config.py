# config.py - configuration constants common to experiments.py and plot.py
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Provides constants which are common to both `experiments.py` and `plot.py`,
including the scheduler identifiers, the total offered load values, the number
of traffic sources, and the number of trials to run.

"""
import logging

SCHEDULERS = 'FIFO', 'RR', 'DRR'
"""The strings identifying the three schedulers to test."""
LOADS = range(4, 22, 2)
"""The total offered loads to test, multiplied by 10 so that they are integers
and can therefore be used as reliable keys in dictionaries.

"""
NUM_SOURCES = 11
"""The number of traffic sources in the simulation.

This is hard-coded in the simulation for now. See
`simulation.simulation.Simulation`.

"""
#NUM_TRIALS, T_ALPHA = 121, 1.658
NUM_TRIALS, T_ALPHA = 5, 2.132
"""NUM_TRIALS is the total number of independent trials to run for each
combination of traffic source, total offered load value, and scheduler type.

T_ALPHA is a value necessary for computing confidence intervals.

The value of T_ALPHA depends on `NUM_TRIALS`, and half the confidence interval
percentage desired, and is looked up from the table at
http://people.hofstra.edu/Stefan_Waner/RealWorld/finitetopic1/t_table.html.

"""


# uncomment this line to get DEBUG messages
#logging.basicConfig(level=logging.DEBUG)
