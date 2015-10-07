#!/bin/sh
#
# run-tests.sh - runs all unit tests for the simulation package
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011

PYTHONPATH=. python -m unittest tests
