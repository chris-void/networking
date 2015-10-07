#!/bin/sh
#
# run-tests.sh - runs all unit tests for the simulation package
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011

PYTHONPATH=. python3 -m unittest tests
