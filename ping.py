#!/usr/bin python
#
# reference for:
#   http://www.g-loaded.eu/2009/10/30/python-ping/

import os
import sys
import socket
import struct
import select
import time

ICMP_ECHO_REQ = 8

def checksum(source_string):
    sum = 0
	countTo = (len(source_string)/2)*2
	count = 0



def verbosePing(dest_addr, timeout = 2, count = 4):
	for i in xrange(count):
		print "ping %s ..." % dest_addr
		try:
			delay = ping(dest_addr, timeout)
		except socket.ga
