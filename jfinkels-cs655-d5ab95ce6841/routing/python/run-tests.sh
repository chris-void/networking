#!/bin/sh
#
# run-tests.sh - runs all unit tests for the routing package
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011

PYTHONPATH=. python3 -m unittest tests
