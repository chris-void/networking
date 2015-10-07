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
import logging
import socket
import socketserver
import sys
import time

PROTOCOL_PHASES = ('s', 'm', 't')
"""Identifying strings for the phases of the protocol: 's' for setup phase,
'm' for measurement phase, and 't' for termination phase.

"""
MEASUREMENT_TYPES = ('rtt', 'tput')
"""Identifiers of types of measurement types used by the client performing the
measurements.

"""
ERR_SETUP = 'Invalid Connection Setup Message'
"""Error message for invalid connection setup message."""
ERR_TERM = 'Invalid Connection Termination Message'
"""Error message for invalid connection termination message."""
ERR_PROT = 'Invalid Protocol Phase Identifier'
"""Error message for invalid protocol phase identifier."""
ERR_EMPTY = 'Empty Message'
"""Error message for an empty message."""
ERR_MEASURE = 'Invalid Measurement Message'
"""Error message for an invalid measurement message."""


class MeasurementProtocolHandler(socketserver.StreamRequestHandler):
    """Handles requests from clients.

    A new instance of this class is created for each connection to the server.

    """

    def handle_setup(self, measurement_type, num_probes, message_size, delay):
        """Prepares this handler for making the requests measurements.

        `measurement_type` may be either `'rtt'` or `'tput'`, representing
        round-trip time and throughput, respectively.

        `num_probes` is the number of probes which the client will send.

        `message_size` is the size of the probes which will be sent, in bytes.

        `delay` is the delay in seconds that this handler should inject before
        sending a response. This may be a floating point number.

        If the input parameters are invalid, sends back the error message:

            404 ERROR: Invalid Connection Setup Message

        Otherwise, sends back the acknowledgment message:

            200 OK: Ready

        """
        try:
            self.num_expected_messages = int(num_probes)
            self.message_size = int(message_size)
            self.delay = float(delay)
        except ValueError:
            logging.debug('responding with error: could not get int')
            self.respond_error(ERR_SETUP)
            self.still_processing = False
            return
        if measurement_type not in MEASUREMENT_TYPES:
            logging.debug('responding with error: bad measurement type')
            self.respond_error(ERR_SETUP)
            self.still_processing = False
            return
        self.measurement_type = measurement_type
        self.current_sequence_num = 1
        logging.debug('responding with OK')
        self.respond_ok('Ready')

    def handle_measurement(self, sequence_num, payload):
        """Echos the specified `payload` bytes, if `sequence_num`, the
        sequence number of this message, is one plus the previous sequence
        number.

        If the sequence is out of order, or the message is otherwise invalid,
        sends back the error message:

            404 ERROR: Invalid Measurement Message

        Otherwise, sends back the payload data unchanged.

        """
        logging.debug('sequence num {}'.format(sequence_num))
        logging.debug('payload {}'.format(payload))
        if int(sequence_num) > self.num_expected_messages:
            logging.debug('too many messages sent')
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        if int(sequence_num) != self.current_sequence_num:
            logging.debug('expected sequence number {}'
                          .format(self.current_sequence_num))
            logging.debug('sequence_num != self.current_seq_num: {}'
                          .format(sequence_num != self.current_sequence_num))
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        if len(payload) != self.message_size:
            logging.debug('expecting payload size {}'
                          .format(self.message_size))
            logging.debug('  got payload size {}'.format(len(payload)))
            logging.debug('len(payload) != self.message_size: {}'
                          .format(len(payload) != self.message_size))
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        self.current_sequence_num += 1
        time.sleep(self.delay)
        self.wfile.write(payload.encode('utf8'))

    def respond_ok(self, message):
        """Sends a response to the client of the form

            200 OK: <message>

        where `<message>` is the specified `message`.

        """
        self.wfile.write('200 OK: {0}'.format(message).encode('UTF-8'))
        logging.debug('responded with OK')

    def respond_error(self, message):
        """Sends a response to the client of the form

            404 ERROR: <message>

        where `<message>` is the specified `message`.

        """
        self.wfile.write('404 ERROR: {0}'.format(message).encode('UTF-8'))

    def handle(self):
        """Handles the incoming request by delegating to one of the protocol
        phase handler functions in this class, depending on the phase
        identifier specified in the incoming message.

        The valid phase specifiers are 's' for setup, 'm' for measurement',
        and 't' for termination.

        **Note**: this function will block until a newline character is read
        from the client's request.

        """
        # Other functions may set this to False in order to stop handling data
        # sent from the client.
        self.still_processing = True
        while self.still_processing:
            logging.debug('handling request')
            received_data = self.rfile.readline().strip()
            # inputs come as `bytes` objects; for ease of use we decode to strings
            incoming = [x.decode() for x in received_data.split()]
            logging.debug('incoming {}'.format(incoming))
            if len(incoming) == 0:
                self.respond_error(ERR_EMPTY)
                break
            phase = incoming[0]
            if phase == 's':
                logging.debug('  handling setup phase')
                if len(incoming[1:]) != 4:
                    self.respond_error(ERR_SETUP)
                    break
                self.handle_setup(*incoming[1:])
            elif phase == 'm':
                logging.debug('  handling measurement phase')
                if len(incoming[1:]) != 2:
                    self.respond_error(ERR_MEASURE)
                    break
                self.handle_measurement(*incoming[1:])
            elif phase == 't':
                logging.debug('  handling termination phase')
                if len(incoming) > 1:
                    self.respond_error(ERR_TERM)
                else:
                    self.respond_ok('Closing Connection')
                break
            else:
                self.respond_error(ERR_PROT)
                break

            
def main(host, port):
    """Creates a TCP socket on the specified address and starts listening for
    requests (forever, until the handler calls the `shutdown()` function.

    """
    server = socketserver.TCPServer((host, port), MeasurementProtocolHandler)
    server.serve_forever()
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.critical('Must specify port on which to run the server.'
                         ' For example:')
        logging.critical('    ./server.py <portnumber>')
        sys.exit(1)
    if len(sys.argv) >= 3 and sys.argv[2] == 'debug':
        logging.basicConfig(level=logging.DEBUG)
    main(socket.getfqdn(), int(sys.argv[1]))
