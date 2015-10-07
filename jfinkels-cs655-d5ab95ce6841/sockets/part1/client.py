#!/usr/bin/env python3
#
# client.py - the echo client
#
# CS655 sockets assignment
# Jeffrey Finkelstein
# October 2011
"""Sends a message to a socket on a specified address.

The first two command-line arguments must be the host and port, respectively,
to which to send the message. All remaining command-line arguments are treated
as the message to send, and are sent to the specified address.

"""
import socket
import sys

if __name__ == '__main__':
    HOST, PORT = sys.argv[1:3]
    data = bytes(' '.join(sys.argv[3:]) + '\n', 'utf8')
    with socket.create_connection((HOST, PORT)) as s:
        s.send(data)
        received = s.recv(1024)
    print("Sent:     %s" % data)
    print("Received: %s" % received)
