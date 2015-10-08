#!/usr/bin/env python3
#
# client.py - runs the experiments
#
# Shuwen Sun
# Oct 2015

import socket
import configparser
import os
import sys
from datetime import datetime

from config import HOST
from config import PORT
from config import RECEIVE_BYTES
from config import NUM_PROBES
from config import NUM_TRIALS
from config import SERVER_DELAYS
from config import MEASUREMENTS

class ServerException(Exception):
    """
    exception for client connct server
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class Statistics(object):
    """
    use send time, recv time and msg size to calculate rtt and tput
    """
    def __init__(self, send_time, recv_time, message_size):
        self.send_time = send_time
        self.recv_time = recv_time
        self.message_size = message_size

    def round_trip_time(self):
        return (self.recv_time - self.send_time).total_seconds()

    def throughput(self):
        return self.message_size / self.round_trip_time()



class ClientProcess(object):
    """
    client process
    implement the function in 3 phases
    """
    def __init__(self, host, port, measurement_type, num_probes, message_size, delay):
        self.host, self.port = host, port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.measurement_type = measurement_type
        self.max_probes = num_probes
        self.message_size = message_size
        self.delay = delay
        self.stats = []

    def __enter__(self):
        self.sock.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()

    def check_for_error(self, data):
        if data.startswith(b'404 ERROR'):
            raise ServerException(data[11:])

    def request_bytes(self, *args, suffix=b'', **kw):
        if suffix:
            suffix = b' ' + suffix
        return ' '.join(args).encode('utf8') + suffix + b'\n'

    def run(self):
        self.send_setup_connection()
        self.send_probes()
        self.send_termination()

    def send_and_recv(self, message):
        self.sock.send(message)
        result = self.sock.recv(RECEIVE_BYTES)
        return result

    def send_probes(self):
        for n in range(1, self.max_probes + 1):
            data = self.request_bytes('m', str(n),
                                      suffix=b'.' * self.message_size)
            time_sent = datetime.now()
            self.sock.send(data)
            received = self.sock.recv(RECEIVE_BYTES)
            while len(received) < self.message_size:
                received += self.sock.recv(RECEIVE_BYTES)
            time_received = datetime.now()
            self.check_for_error(received)
            result = Statistics(time_sent, time_received, self.message_size)
            self.stats.append(result)

    def send_setup_connection(self):
        data = self.request_bytes('s', self.measurement_type,
                                  str(self.max_probes), str(self.message_size),
                                  str(self.delay))
        result = self.send_and_recv(data)
        self.check_for_error(result)

    def send_termination(self):
        result = self.send_and_recv(b't \n')
        self.check_for_error(result)

def main(host, port):
    results = {}
    for d in SERVER_DELAYS:
        results[d] = {}
        for m, sizes in MEASUREMENTS.items():
            results[d][m] = {}
            for s in sizes:
                results[d][m][s] = {}
                for n in range(NUM_TRIALS):
                    with ClientProcess(host, int(port), m, NUM_PROBES, s, d) as e:
                        e.run()
                        if m == 'rtt':
                            data = [x.round_trip_time() for x in e.stats]
                        else:
                            data = [x.throughput() for x in e.stats]
                        results[d][m][s][n] = data
    write_results(results)


def write_results(results, f=sys.stdout):
    f.write('# written at {}\n'.format(datetime.now().isoformat()))
    f.write('# delay measurement_type msg_size trial_num probe_num value\n')
    for delay in SERVER_DELAYS:
        for m, sizes in MEASUREMENTS.items():
            for size in sizes:
                for trial_num in range(NUM_TRIALS):
                    values = results[delay][m][size][trial_num]
                    assert len(values) == NUM_PROBES
                    for probe_num in range(NUM_PROBES):
                        f.write(' '.join(('{}' for n in range(6)))
                                .format(delay, m, size, trial_num, probe_num,
                                        values[probe_num]))
                        f.write('\n')


if __name__ == '__main__':
    main(HOST, PORT)
