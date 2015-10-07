# __init__.py - provides all unit tests for the `routing` package
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides all unit tests for the `routing` package."""
import logging
logging.basicConfig(level=logging.CRITICAL)

from .test_protocols import *
from .test_random import *
from .test_simulation import *
