# plot.py - creates and displays average round-trip time plots
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Creates and displays average round-trip time plots.

This script requires the Python libraries `matplotlib` and `numpy`.

By default, this file reads the output from the `experiments.py` script from
standard input. If a filename is specified as a command-line argument, then the
results will be read from that file. For example::

    python plot.py results.out

This script requires Python 2.7.

"""
from datetime import datetime
import itertools
import logging
import math
import os
import os.path
import shutil
import sys

from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib.pyplot as plt

from config import PROTOCOLS
from config import CORRUPTION_PROBS
from config import LOSS_PROBS
from config import NUM_TRIALS
from config import T_ALPHA
from config import NUM_MESSAGES
from config import MESSAGE_DELAY
from config import WINDOWSIZE
from config import TIMEOUT

OUTPUT_DIR = 'output'
"""The directory in which to store output plots."""
DATE_FORMAT = '%Y-%m-%d-%H-%M-%S'
"""The format for date string when creating a directory based on the time at
which this script is executed.

"""
BAR_WIDTH = 0.04
"""The width of the plotted bars."""

# uncomment this line to get debugging messages
logging.basicConfig(level=logging.DEBUG)


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
    """Returns an empty four-dimensional table, of the form

        table[protocol][corruption][loss][trial_num] = None

    """
    return dict([(protocol,
                  dict([(corr,
                         dict([(loss,
                                dict([(num_trial, None)
                                      for num_trial in range(NUM_TRIALS)]))
                               for loss in LOSS_PROBS]))
                        for corr in CORRUPTION_PROBS]))
                 for protocol in PROTOCOLS])

def initialize_stats_table():
    """Returns an empty three-dimensional table, of the form

        table[protocol][corruption][loss] = None

    """
    return dict([(protocol,
                  dict([(corr,
                         dict([(loss, None) for loss in LOSS_PROBS]))
                        for corr in CORRUPTION_PROBS]))
                 for protocol in PROTOCOLS])


if __name__ == '__main__':
    data = data_from_args()
    data = map(lambda l: l.strip(), data)
    data = filter(lambda l: not l.startswith('#'), data)
    data = filter(lambda l: len(l) > 0, data)
    results = initialize_results_table()
    # get the mean RTT as it depends on protocol, corruption, loss, and trial
    for line in data:
        (protocol, corr, loss, trial_num, num_sent, tput, gput, mean_rtt,
         retrans, num_corr, num_loss) = line.split()
        corr = float(corr)
        loss = float(loss)
        trial_num = int(trial_num)
        num_sent = int(num_sent)
        tput = float(tput)
        gput = float(gput)
        mean_rtt = float(mean_rtt)
        retrans = int(retrans)
        num_corr = int(num_corr)
        num_loss = int(num_loss)
        results[protocol][corr][loss][trial_num] = mean_rtt
    # compute the mean and variance for RTT as it depends on protocol,
    # corruption, and loss
    averages = initialize_stats_table()
    variances = initialize_stats_table()
    confidences = initialize_stats_table()
    for p in PROTOCOLS:
        for c in CORRUPTION_PROBS:
            for l in LOSS_PROBS:
                averages[p][c][l] = numpy.mean(results[p][c][l].values())
                variances[p][c][l] = numpy.var(results[p][c][l].values())
                confidences[p][c][l] = (T_ALPHA * variances[p][c][l]
                                        / math.sqrt(NUM_TRIALS))
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    outdir = os.path.join(OUTPUT_DIR, datetime.now().strftime(DATE_FORMAT))
    os.mkdir(outdir)
    # copy the configuration and results file there for later reference
    shutil.copy('config.py', os.path.join(outdir, 'config.py'))
    with open(os.path.join(outdir, 'data'), 'w') as f:
        f.writelines((line + '\n' for line in data))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plotted_bars = []
    for (p, color, shift) in zip(PROTOCOLS, ('r', 'b'), (0, BAR_WIDTH)):
        first_time = True
        for z in LOSS_PROBS:
            xs = [c + shift for c in CORRUPTION_PROBS]
            ys = [averages[p][c][z] for c in CORRUPTION_PROBS]
            yerr = [confidences[p][c][z] for c in CORRUPTION_PROBS]
            # see matplotlib.axes.Axes.bar() to figure out error bars...
            logging.debug('averages for loss prob {}: {}'.format(z, ys))
            logging.debug('errors for loss prob {}: {}'.format(z, yerr))
            bars = ax.bar(xs, ys, zs=z, zdir='y', alpha=0.75, color=color,
                          width=BAR_WIDTH)
            plotted_bars.extend(bars)
            # draw the error bars
            if p == 'SR':
                for (x, y, e) in zip(CORRUPTION_PROBS, ys, yerr):
                    _x = x + (BAR_WIDTH / 2) + shift
                    ax.plot([_x, _x], [y - e, y + e], zs=z, zdir='y', color='black')
    ax.legend((plotted_bars[0], plotted_bars[-1]),
              ('go back N', 'selective repeat'), loc='upper left')
    ax.set_xlim3d(0, 0.6)
    ax.set_ylim3d(0, 0.6)
    ax.set_xlabel('corruption probability')
    ax.set_ylabel('loss probability')
    ax.set_zlabel('average round-trip time')
    plt.suptitle('average round-trip time as it depends on \ncorruption'
                 ' probability and loss probability, for each protocol\n'
                 '(retransmission timeout {}, window size {}, avg. message delay {},'
                 ' {} total messages sent)'.format(TIMEOUT, WINDOWSIZE, MESSAGE_DELAY,
                                                   NUM_MESSAGES))

    plt.savefig(os.path.join(outdir, 'rtts.png'))
    logging.debug('...saved rtts.png')
