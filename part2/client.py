#!/usr/bin/env python3
#
# client.py - runs the experiments
#
# CS655 sockets assignment
# Jeffrey Finkelstein
# October 2011
"""Runs the experiments described in the assignment.

This module should be run as a main module. The first two command-line
arguments must be the host and port, respectively, on which the server is
running. For example:

    ./client.py example.com 1234

"""
from datetime import datetime
import logging
import sys

from config import NUM_PROBES
from config import NUM_TRIALS
from config import SERVER_DELAYS
from config import MEASUREMENTS
from experiment import Experiment


def main(host, port):
    """Runs the experiments described in the assignment with all possible sets
    of parameters, with messages sent to the server on the specified host and
    port.

    """
    results = {}
    for d in SERVER_DELAYS:
        results[d] = {}
        for m, sizes in MEASUREMENTS.items():
            results[d][m] = {}
            for s in sizes:
                results[d][m][s] = {}
                for n in range(NUM_TRIALS):
                    with Experiment(host, int(port), m, NUM_PROBES, s, d) as e:
                        logging.debug('*** new experiment')
                        logging.debug('trial: {}'.format(n))
                        logging.debug('host: {}'.format(host))
                        logging.debug('port: {}'.format(port))
                        logging.debug('measurement: {}'.format(m))
                        logging.debug('probes: {}'.format(NUM_PROBES))
                        logging.debug('message size: {}'.format(s))
                        logging.debug('server delay: {}'.format(d))
                        e.run()
                        if m == 'rtt':
                            data = [x.round_trip_time() for x in e.stats]
                        else:
                            data = [x.throughput() for x in e.stats]
                        results[d][m][s][n] = data
                        logging.debug('observations: {}'
                                      .format(results[d][m][s][n]))
    write_results(results)


def write_results(results, f=sys.stdout):
    """Writes the results table to the file-like object `f`.

    The elements of the results table must be accessible by the expression::

        results[delay][measurement_type][message_size][trial_num]

    and the value of that expression is a list of length `NUM_PROBES`
    containing the measured values of type `measurement_type`.

    """
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
    if len(sys.argv) < 3:
        logging.critical('Must specify host and port on which the server is'
                         ' running. For example:')
        logging.critical('    ./client.py <hostname> <portnumber>')
        sys.exit(1)
    if len(sys.argv) >= 4 and sys.argv[3].lower() == 'debug':
        logging.basicConfig(level=logging.DEBUG)
    host, port = sys.argv[1:3]
    main(host, port)
