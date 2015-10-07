# __init__.py - provides all unit test classes
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Provides all unit test classes."""
import logging
# uncomment this line to get debug messages in tests
#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

from test_analysis import *
from test_endpoints import *
from test_runner import *
from test_schedulers import *
