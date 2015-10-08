#!/usr/bin/env python3
#
# server.py - runs the experiments
#
# Shuwen Sun
# Oct 2015

import socket
import socketserver
import sys
import time

PROTOCOL_PHASES = ('s', 'm', 't')
MEASUREMENT_TYPES = ('rtt', 'tput')

ERR_SETUP = 'Invalid Connection Setup Message'
ERR_TERM = 'Invalid Connection Termination Message'
ERR_PROT = 'Invalid Protocol Phase Identifier'
ERR_EMPTY = 'Empty Message'
ERR_MEASURE = 'Invalid Measurement Message'


class MeasurementProtocolHandler(socketserver.StreamRequestHandler):
    def handler_setup(self, measurement_type, num_probes, message_size, delay):
        try:
            self.num_expected_messages = int(num_probes)
            self.message_size = int(message_size)
            self.delay = float(delay)
        except ValueError:
            self.respond_error(ERR_SETUP)
            self.still_processing = False
            return
        if measurement_type not in MEASUREMENT_TYPES:
            self.respond_error(ERR_SETUP)
            self.still_processing = False
            return
        self.measurement_type = measurement_type
        self.current_sequence_num = 1
        self.respond_ok('Ready')

    def handler_measurement(self, sequence_num, payload):
        if int(sequence_num) > self.num_expected_messages:
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        if int(sequence_num) != self.current_sequence_num:
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        if len(payload) != self.message_size:             
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        self.current_sequence_num += 1
        time.sleep(self.delay)
        self.wfile.write(payload.encode('utf8'))

    def respond_ok(self, message):
        self.wfile.write('200 OK: {0}'.format(message).encode('UTF-8'))

    def respond_error(self, message):
        self.wfile.write('404 ERROR: {0}'.format(message).encode('UTF-8'))

    def handler(self):
        # sent from the client.
        self.still_processing = True
        while self.still_processing:
            received_data = self.rfile.readline().strip()
            incoming = [x.decode() for x in received_data.split()]
            if len(incoming) == 0:
                self.respond_error(ERR_EMPTY)
                break
            phase = incoming[0]
            if phase == 's':
                if len(incoming[1:]) != 4:
                    self.respond_error(ERR_SETUP)
                    break
                self.handler_setup(*incoming[1:])
            elif phase == 'm':
                if len(incoming[1:]) != 2:
                    self.respond_error(ERR_MEASURE)
                    break
                self.handler_measurement(*incoming[1:])
            elif phase == 't':
                if len(incoming) > 1:
                    self.respond_error(ERR_TERM)
                else:
                    self.respond_ok('Closing Connection')
                break
            else:
                self.respond_error(ERR_PROT)
                break

            
def main(host, port):
    server = socketserver.TCPServer((host, port), MeasurementProtocolHandler)
    server.serve_forever()
    
if __name__ == "__main__":
    main(socket.getfqdn(), int(sys.argv[1]))
