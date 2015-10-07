# experiments.py - runs the experiments required by the assignment
#
# CS655 error control assignment
# Jeffrey Finkelstein
# November 2011
"""Runs the experiments required by the assignment.

This script measures and outputs, for each protocol, the average round-trip
time for packets sent with corruption probability and loss probability varying
by 0.1 from 0.0 to 0.5, inclusive. Multiple independent trials of the
simulation are performed.

This script outputs the table of results to standard output. If a filename is
specified as a command-line argument, then the results will be written to that
file. For example::

    python3 experiments.py results.out

This script requires Python 3.2.

"""

from datetime import datetime
import itertools
from multiprocessing import cpu_count
from multiprocessing import Pool
import sys

from config import CORRUPTION_PROBS
from config import LOSS_PROBS
from config import MESSAGE_DELAY
from config import NUM_MESSAGES
from config import NUM_TRIALS
from config import PROTOCOLS
from config import TIMEOUT
from config import TRACE
from config import WINDOWSIZE
from simulation.runner import run_parameterized_simulation as run_simulation


def run_experiment(arguments, *args, **kw):
    """Runs a single experiment simulation with the specified arguments:

    The `arguments` parameter must be a 4-tuple of the form `(protocol,
    corruption, loss, trial_num)`, where::

    * `protocol` is one of `GBN`, `SR`, or `AB`,
    * `corruption` and `loss` are floating point numbers between 0 and 1, and
    * `trial_num` is the ID of the trial.

    The other positional and keyword arguments are passed on to the
    `simulation.runner.run_simulation` function.  Returns the
    `simulation.runner.Results` object which results from running a simulation
    with the specified properties.

    """
    protocol, corruption_prob, loss_prob, trial_number = arguments
    return run_simulation(protocol=protocol,
                          corruption_probability=corruption_prob,
                          loss_probability=loss_prob,
                          num_messages=NUM_MESSAGES, avg_delay=MESSAGE_DELAY,
                          trace=TRACE, windowsize=WINDOWSIZE, timeout=TIMEOUT)


def write_results(results_table, start_time, f=sys.stdout):
    """Writes the data from the table of results to the file-like object `f`.

    The output is a sequence of lines reqpresenting records from the specified
    table of results. The format of each line of the output (except for lines
    starting with an initial hash [#], which are comments) is

        <protocol> <corruption> <loss> <tral_num> <num_sent> <throughput> \
          <goodput> <mean_rtt> <num_retransmitted> <num_corrupt> <num_lost>

    """
    f.write('# experiments started at {0}\n'.format(start_time))
    f.write('# written at {0}\n'.format(datetime.now().isoformat()))
    f.write('# protocol corruption loss trial_num num_sent throughput goodput'
            ' mean_rtt num_retransmitted num_corrupt num_lost\n')
    for protocol in PROTOCOLS:
        for loss in LOSS_PROBS:
            for corr in CORRUPTION_PROBS:
                for run in range(NUM_TRIALS):
                    stats = results[protocol][corr][loss][run]
                    f.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n'
                            .format(protocol, corr, loss, run, stats.num_sent,
                                    stats.throughput, stats.goodput,
                                    stats.mean_rtt, stats.num_retransmitted,
                                    stats.num_corrupt, stats.num_lost))

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


if __name__ == '__main__':
    start_time = datetime.now().isoformat()
    parameters = list(itertools.product(PROTOCOLS, CORRUPTION_PROBS,
                                        LOSS_PROBS, range(NUM_TRIALS)))
    try:
        num_processes = cpu_count()
    except NotImplementedError:
        num_processes = 1
    pool = Pool(min(num_processes, len(parameters)))
    temp_results = pool.map(run_experiment, parameters)
    results = initialize_results_table()
    for p, r in zip(parameters, temp_results):
        results[p[0]][p[1]][p[2]][p[3]] = r
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as f:
            write_results(results, start_time, f)
    else:
        write_results(results, start_time)
