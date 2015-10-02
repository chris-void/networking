#!/usr/bin/env python

# Echo server program
import socket

HOST = '128.197.11.36'                 # Symbolic name meaning the local host
PORT = 58909              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print "Server Started"

conn, addr = s.accept()
print 'Connexcted by', addr

while 1:
    data = conn.recv(1024)
    if not data: break
    print "Data Received:", data
    conn.send(data)

conn.close()
