#!/usr/bin/env python3
#
# server.py - the echo server
#
# CS655 sockets assignment
# Jeffrey Finkelstein
# October 2011
"""Receives and echos messages from clients connected to a specified TCP
socket.

The sole command-line argument is the port number on the current host at which
the socket will be created.

"""
import socket
import socketserver
import sys

class EchoHandler(socketserver.StreamRequestHandler):
    """Handles requests from clients.

    A new instance of this class is created for each request.

    """

    def handle(self):
        """Sends the data from the request back to the sending client."""
        self.data = self.rfile.readline().strip()
        self.wfile.write(self.data)

if __name__ == "__main__":
    HOST, PORT = socket.getfqdn(), int(sys.argv[1])
    server = socketserver.TCPServer((HOST, PORT), EchoHandler)
    server.serve_forever()
