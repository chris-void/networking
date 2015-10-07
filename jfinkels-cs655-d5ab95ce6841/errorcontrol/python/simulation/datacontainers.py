# datacontainers.py - classes which wrap a string message
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Provides classes representing objects which encapsulate a string message,
such as a `Message` from layer 5, or a `Packet` on the link between hosts.

"""

MAX_DATA_SIZE = 20
"""The maximum length of a string which can be the data in one of the data
container classes in this module.

"""


class DataContainer(object):
    """An object which stores a string of size at most `MAX_DATA_SIZE`."""

    def __init__(self, data):
        """Instantiates this container to contain the specified string of
        length at most `MAX_DATA_SIZE`.

        """
        if data is None or len(data) > MAX_DATA_SIZE:
            self.data = ''
        else:
            self.data = data


class Message(DataContainer):
    """A message to (from) layer 5 passed from (to) the sender's (receiver's)
    reliable data transfer layer.

    """
    pass


class Packet(DataContainer):
    """A packet which travels along the unreliable data link."""

    def __init__(self, sequence_number, ack_number, checksum, payload=None):
        """Initializes the packet containing the string `payload` as data,
        with the specified sequence number, ACK number, and checksum.

        """
        super().__init__(payload)
        self.seqnum = sequence_number
        self.acknum = ack_number
        self.checksum = checksum

    def __str__(self):
        """Returns the string representation of this packet."""
        return ('Packet[seqnum {}, acknum {}, checksum {}, payload {}]'
                .format(self.seqnum, self.acknum, self.checksum, self.data))

    def __repr__(self):
        return str(self)
