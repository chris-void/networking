#!/usr/bin/env python


import socket
import sys
import struct

def connect(addr, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr,port))
        return (0, s)
    except socket.error, (value,message):
        if s:
            s.close()
        return (-1, message)


def sendMsg(conn, msg):
    if msg=="":
        return (-1, "Cannot send empty string.")
    size = 1024
    try:
        conn.sendall(msg)
        return (0, None)
    except socket.error, (value,message):
        conn.close()
        return (-1, message)

def sendNum(conn, num):
    msg = struct.pack("<i", num)
    size = 1024
    try:
        conn.sendall(msg)
        return (0, None)
    except socket.error, (value,message):
        conn.close()
        return (-1, message)

def recvMsg(conn):
    size = 1024
    try:
        data = conn.recv(size)
        return (0, data)
    except socket.error, (value,message):
        conn.close()
        return (-1, message)

def close(conn):
    try:
        conn.close()
        return (0, None)
    except socket.error, (value,message):
        return (-1, message)


