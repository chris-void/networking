#!/usr/bin/env python

# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 58909          # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send('Hello, world')
data = s.recv(1024)


print 'Received From Server:', repr(data)
