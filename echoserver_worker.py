
import sys, traceback, threading, socket
import struct
import random

size = 1024

class ServerWorker:

    def __init__(self, clientInfo):
        self.clientInfo = clientInfo
        self.connSocket = self.clientInfo['socket'][0]
        self.clientAddr = self.clientInfo['socket'][1]
		
    def run(self):
        print "running worker"
        threading.Thread(target=self.work0).start()

    def work0(self):
        print self.clientAddr, "has connected."
        try:
            while 1:
                data = self.connSocket.recv(size)
                print self.clientAddr, "sends:", data
                if data == "":
                    break
                self.connSocket.sendall(data)
        except socket.error, (code, message):
                    print "error processing client", self.clientAddr
        finally:
            print "work is done"
            if self.connSocket:
                self.connSocket.close()




