# plot.py - creates and displays throughput and packet latency plots
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Creates and displays throughput difference and packet latency plots.

This script requires the Python libraries `matplotlib` and `numpy`.

By default, this file reads the output from the `experiments.py` script from
standard input. If a filename is specified as a command-line argument, then the
results will be read from that file. For example::

    python plot.py results.out

"""
from datetime import datetime
import logging
import math
import os
import os.path
import shutil
import sys

import matplotlib.pyplot as plt
import numpy

from config import SCHEDULERS
from config import LOADS
from config import NUM_SOURCES
from config import NUM_TRIALS
from config import T_ALPHA

OUTPUT_DIR = 'output'
"""The directory in which to store output plots."""
DATE_FORMAT = '%Y-%m-%d-%H-%M-%S'
"""The format for date string when creating a directory based on the time at
which this script is executed.

"""
# uncomment this line to get debugging messages
#logging.basicConfig(level=logging.DEBUG)


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


def initialize_results_table():
    """Returns an empty four-dimensional table, one dimension each for
    scheduler type, total offered load value, source number, and trial number.

    The returned table is of the form

        >>> results[scheduler][load][source_id][trial_num] = None

    """
    results = {}
    for scheduler in SCHEDULERS:
        results[scheduler] = {}
        for load in LOADS:
            results[scheduler][load] = {}
            for source_id in range(NUM_SOURCES):
                results[scheduler][load][source_id] = {}
                for trial_num in range(NUM_TRIALS):
                    results[scheduler][load][source_id][trial_num] = None
    return results


if __name__ == '__main__':
    data = data_from_args()
    data = map(lambda l: l.strip(), data)
    data = filter(lambda l: not l.startswith('#'), data)
    data = filter(lambda l: len(l) > 0, data)
    results = initialize_results_table()
    source_types = {}
    for line in data:
        (sched, load, source_id, source_type, trial_num, throughput, diff,
         ratio, latency) = line.split()
        load_10 = int(10 * float(load))
        source_id = int(source_id)
        trial_num = int(trial_num)
        throughput = float(throughput)
        diff = float(diff)
        ratio = float(ratio)
        latency = float(latency)
        results[sched][load_10][source_id][trial_num] = (ratio, latency)
        if source_id not in source_types:
            source_types[source_id] = source_type
    # determine the throughputs and latencies
    stats = {}
    for s in SCHEDULERS:
        stats[s] = {}
        for i in range(NUM_SOURCES):
            stats[s][i] = {}
            for l in LOADS:
                stats[s][i][l] = {}
                vals = [results[s][l][i][n] for n in range(NUM_TRIALS)]
                throughputs, latencies = zip(*vals)
                # stats[s][i][l]['throughputs'] has a list of throughput ratios
                # corresponding to results from individual trials for scheduler
                # s, source i, and load l
                stats[s][i][l]['throughputs'] = throughputs
                stats[s][i][l]['latencies'] = latencies
    # compute the means and variances as they depend on load
    averages = {}
    variances = {}
    for s in SCHEDULERS:
        averages[s] = {}
        variances[s] = {}
        for i in range(NUM_SOURCES):
            averages[s][i] = {}
            variances[s][i] = {}
            for d in 'throughputs', 'latencies':
                # If d is 'throughputs' then averages[s][i][d] a list of mean
                # throughputs (where the mean is over NUM_TRIALS trials), where
                # each mean throughput in the list corresponds to a value for
                # total offered load; same for 'latencies'.
                #
                # If t_l is the mean throughput over NUM_TRIALS trials for load
                # l, then the list of loads is [4, 6, 8, ..., 20] and the
                # corresponding averages[s][i][d] list is [t_4, t_6, t_8, ...,
                # t_20].
                #
                # variances[s][i][d] is the same, but with variance instead of
                # mean.
                averages[s][i][d] = [numpy.mean(stats[s][i][l][d])
                                     for l in LOADS]
                variances[s][i][d] = [numpy.var(stats[s][i][l][d])
                                      for l in LOADS]

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    outdir = os.path.join(OUTPUT_DIR, datetime.now().strftime(DATE_FORMAT))
    os.mkdir(outdir)
    # copy the configuration and results file there for later reference
    shutil.copy('config.py', os.path.join(outdir, 'config.py'))
    with open(os.path.join(outdir, 'data'), 'w') as f:
        f.writelines(data)

    loads = [l / 10.0 for l in LOADS]
    for i in range(NUM_SOURCES):
        for d, dlabel in (('throughputs',
                           'throughput ratio (measured:expected)'),
                          ('latencies', 'latency ($sec$)')):
            logging.debug('plotting source {0} {1}...'.format(i, d))
            plotted_lines = []
            for s in SCHEDULERS:
                averages_for_scheduler = averages[s][i][d]
                vars_for_sched = variances[s][i][d]
                confidences = [vars_for_sched[n] for n in range(len(loads))]
                confidence_intervals = [T_ALPHA * c / math.sqrt(NUM_TRIALS)
                                        for c in confidences]
                logging.debug('  scheduler {0} load {1}: {2}'
                              .format(s, l, averages_for_scheduler))
                # HACK the confidence intervals are orders of magnitude larger
                # than the latency values themselves, so plotting them reduces
                # the lines to a straight line at 0 for all schedulers
                if d == 'latencies':
                    confidence_intervals = None
                lines = plt.errorbar(loads, averages_for_scheduler,
                                     yerr=confidence_intervals,
                                     linestyle='-', marker='o')
                # append just the plotted values, not the error bars
                plotted_lines.append(lines[0])
            plt.figlegend(plotted_lines, SCHEDULERS, 'upper right')
            plt.xlabel('total offered load')
            plt.ylabel(dlabel)
            t = source_types[i]
            plt.suptitle('source {0} ({1}) {2} for each scheduler\nas it'
                         ' depends on total offered load'.format(i, t, dlabel))
            plt.savefig(os.path.join(outdir, 'source{0}_{1}.png'.format(i, d)))
            logging.debug('...saved source {0} {1}'.format(i, d))
            plt.clf()
