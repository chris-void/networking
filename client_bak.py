#!/usr/bin/env python

# Echo client program
import socket

HOST = '128.197.11.36'    # The remote host
PORT = 58909          # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send('Hello, world')
data = s.recv(1024)
s.close()

print 'Received From Server:', repr(data)
