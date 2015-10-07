# __init__.py - provides all unit tests for the `simulation` package
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides all unit tests for the `simulation` package."""
import logging
logging.basicConfig(level=logging.CRITICAL)

from .test_endpoints import *
from .test_links import *
from .test_random import *
from .test_simulation import *
