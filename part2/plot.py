#!/usr/bin/env python2.7
#
# plot.py - creates the plots
#
# CS655 sockets assignment
# Jeffrey Finkelstein
# October 2011
from datetime import datetime
import os
import os.path
import shutil
import sys

import matplotlib.pyplot as plt
import numpy

from config import NUM_PROBES
from config import NUM_TRIALS
from config import SERVER_DELAYS
from config import MEASUREMENTS

OUTPUT_DIR = 'output'
"""The directory in which to write the output plots."""
DATE_FORMAT = '%Y-%m-%d-%H-%M-%S'
"""The format for date string when creating a directory based on the time at
which this script is executed.

"""
XLABEL = 'message size (bytes)'
"""The human-readable label for the x-axis in the output plots."""
MEASUREMENT_LABELS = dict(rtt='round-trip time ($ms$)',
                          tput='throughput ($KiB/s$)')
"""The human-readable labels for the y-axis in the output plots."""


def in_kb(value):
    """Returns the specified number of bytes in kibibytes (KiB), that is
    **(value / 2 ^ 10)**.

    """
    return value / (2 ** 10)


def in_ms(value):
    """Returns the specified number of seconds in milliseconds (ms), that is
    **value * 1000**.

    """
    return value * 1000


def data_from_args():
    """Read lines from standard input, or if a filename is specified as the
    first command-line argument, read the lines from that file.

    Returns a list of all strings (including comment lines).

    """
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            return f.readlines()
    else:
        return sys.stdin.readlines()


def plot_results(results, outdir):
    """Creates and saves the plots for the specified table of results.

    The plots are saved under the directory named by `outdir`.

    The input table `results` is of the form:

        >>> results[delay][msrmnt_type][msg_size][trial_num][probe_num] = value

    """
    for d in SERVER_DELAYS:
        for m, sizes in MEASUREMENTS.items():
            means_per_size = []
            for s in sizes:
                # the averages over all probe numbers for each trial
                means_per_trial = [numpy.mean(results[d][m][s][n].values())
                                   for n in range(NUM_TRIALS)]
                # the overall mean over all trials
                means_per_size.append(numpy.mean(means_per_trial))
            if m == 'tput':
                means_per_size = [in_kb(mean) for mean in means_per_size]
            elif m == 'rtt':
                means_per_size = [in_ms(mean) for mean in means_per_size]
            line = plt.plot(sizes, means_per_size, linestyle='-', marker='o')
            plt.xlabel(XLABEL)
            plt.ylabel(MEASUREMENT_LABELS[m])
            plt.suptitle('{} as it depends on {} with server delay {}s'
                         .format(MEASUREMENT_LABELS[m], XLABEL, d))
            plt.savefig(os.path.join(outdir, '{}_delay{}.png'.format(m, d)))
            plt.clf()


def initialize_results_table():
    """Returns an empty four-dimensional table, one dimension each for
    server delay, message size, measurement type, and trial number.

    The returned table is of the form

        >>> results[delay][msrmnt_type][msg_size][trial_num][probe_num] = None

    """
    results = {}
    for d in SERVER_DELAYS:
        results[d] = {}
        for m, sizes in MEASUREMENTS.items():
            results[d][m] = {}
            for s in sizes:
                results[d][m][s] = {}
                for n in range(NUM_TRIALS):
                    results[d][m][s][n] = {}
                    for p in range(NUM_PROBES):
                        results[d][m][s][n][p] = None
    return results


def main():
    data = data_from_args()
    data = map(lambda l: l.strip(), data)
    data = filter(lambda l: not l.startswith('#'), data)
    data = filter(lambda l: len(l) > 0, data)
    results = initialize_results_table()
    for line in data:
        (delay, measurement_type, message_size, trial_num, probe_num, value) \
            = line.split()
        d = float(delay)
        msg_size = int(message_size)
        trial_num = int(trial_num)
        probe_num = int(probe_num)
        value = float(value)
        results[d][measurement_type][msg_size][trial_num][probe_num] = value
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    outdir = os.path.join(OUTPUT_DIR, datetime.now().strftime(DATE_FORMAT))
    os.mkdir(outdir)
    # copy the configuration and results to a file there for later reference
    shutil.copy('config.py', os.path.join(outdir, 'config.py'))
    with open(os.path.join(outdir, 'data'), 'w') as f:
        f.writelines([line + '\n' for line in data])
    plot_results(results, outdir)

if __name__ == '__main__':
    main()
