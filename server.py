

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
    def handle_setup(self, measurement_type, num_probes, message_size, delay):
        try:
            self.num_expected_messages = int(num_probes)
            self.message_size = int(message_size)
            self.delay = float(delay)
        except ValueError:
            #logging.debug('responding with error: could not get int')
            self.respond_error(ERR_SETUP)
            self.still_processing = False
            return
        if measurement_type not in MEASUREMENT_TYPES:
            #logging.debug('responding with error: bad measurement type')
            self.respond_error(ERR_SETUP)
            self.still_processing = False
            return
        self.measurement_type = measurement_type
        self.current_sequence_num = 1
        #logging.debug('responding with OK')
        self.respond_ok('Ready')

    def handle_measurement(self, sequence_num, payload):
        #logging.debug('sequence num {}'.format(sequence_num))
        #logging.debug('payload {}'.format(payload))
        if int(sequence_num) > self.num_expected_messages:
            #logging.debug('too many messages sent')
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        if int(sequence_num) != self.current_sequence_num:
            #3logging.debug('expected sequence number {}'
            #              .format(self.current_sequence_num))
            #logging.debug('sequence_num != self.current_seq_num: {}'
             #             .format(sequence_num != self.current_sequence_num))
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        if len(payload) != self.message_size:
            #logging.debug('expecting payload size {}'
             #             .format(self.message_size))
            #logging.debug('  got payload size {}'.format(len(payload)))
            #logging.debug('len(payload) != self.message_size: {}'
            #              .format(len(payload) != self.message_size))
            self.respond_error(ERR_MEASURE)
            self.still_processing = False
            return
        self.current_sequence_num += 1
        time.sleep(self.delay)
        self.wfile.write(payload.encode('utf8'))

    def respond_ok(self, message):
        self.wfile.write('200 OK: {0}'.format(message).encode('UTF-8'))
        #logging.debug('responded with OK')

    def respond_error(self, message):
        self.wfile.write('404 ERROR: {0}'.format(message).encode('UTF-8'))

    def handle(self):
        # Other functions may set this to False in order to stop handling data
        # sent from the client.
        self.still_processing = True
        while self.still_processing:
            #logging.debug('handling request')
            received_data = self.rfile.readline().strip()
            # inputs come as `bytes` objects; for ease of use we decode to strings
            incoming = [x.decode() for x in received_data.split()]
            #logging.debug('incoming {}'.format(incoming))
            if len(incoming) == 0:
                self.respond_error(ERR_EMPTY)
                break
            phase = incoming[0]
            if phase == 's':
            #    logging.debug('  handling setup phase')
                if len(incoming[1:]) != 4:
                    self.respond_error(ERR_SETUP)
                    break
                self.handle_setup(*incoming[1:])
            elif phase == 'm':
             #   logging.debug('  handling measurement phase')
                if len(incoming[1:]) != 2:
                    self.respond_error(ERR_MEASURE)
                    break
                self.handle_measurement(*incoming[1:])
            elif phase == 't':
              #  logging.debug('  handling termination phase')
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
    if len(sys.argv) < 2:
        #logging.critical('Must specify port on which to run the server.'
                         ' For example:')
        #logging.critical('    ./server.py <portnumber>')
        sys.exit(1)
    if len(sys.argv) >= 3 and sys.argv[2] == 'debug':
        #logging.basicConfig(level=logging.DEBUG)
    main(socket.getfqdn(), int(sys.argv[1]))
