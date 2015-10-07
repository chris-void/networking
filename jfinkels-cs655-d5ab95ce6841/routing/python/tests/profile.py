# profile.py - runs a profiler on the simulation for debugging purposes
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Profiles a single run of a simulation and prints the results, for debugging
purposes.

"""
import cProfile
import logging

from routing.runner import run_parameterized_simulation as run_simulation


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    cProfile.run("run_simulation(trace=-1, seed=3322, link_changes=False)",
                 sort='time')
