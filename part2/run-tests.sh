#!/bin/sh
#
# run-tests.sh - runs unit tests for the client and server
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011

PYTHONPATH=. python3 -m unittest tests
