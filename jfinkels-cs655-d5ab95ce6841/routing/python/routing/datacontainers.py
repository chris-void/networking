# datacontainers.py - provides packets for communication on a network
#
# CS655 routing assignment
# Jeffrey Finkelstein
# November 2011
"""Provides classes representing objects which encapsulate messages to be sent
along a network.

"""
import copy


class Packet(object):
    """A packet which travels along the unreliable data link."""

    def __init__(self, source, dest, mincosts):
        """Initializes this packet with source ID, destination ID, and table
        of minimum costs (a list of integers).

        Stores a deep copy of the mincosts list.

        """
        self.source = source
        self.dest = dest
        self.mincosts = copy.deepcopy(mincosts)

    def __str__(self):
        """Returns the string representation of this packet."""
        return ('Packet[source {}, dest {}, mincosts {}]'
                .format(self.source, self.dest, self.mincosts))

    def __repr__(self):
        """Returns the string representation of this packet."""
        return str(self)
