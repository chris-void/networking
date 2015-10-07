# experiments.py - runs the experiments specified in the assignment
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Runs the specific experiments described in the assignment.

This script requires the Python library `SimPy`.

For each of the eleven traffic sources, measure, as it depends on total offered
load varied from 0.4 to 2.0 in increments of 0.2:
* the ratio of its measured throughput to its expected throughput
* the average latency of its packets

This script outputs the table of results to standard output. If a filename is
specified as a command-line argument, then the results will be written to that
file. For example::

    python experiments.py results.out

"""
from datetime import datetime
import itertools
from multiprocessing import Pool
from multiprocessing import cpu_count
import sys

from config import SCHEDULERS
from config import LOADS
from config import NUM_SOURCES
from config import NUM_TRIALS
from simulation.runner import run_parameterized_simulation as run_simulation
from simulation.runner import TelnetSource
from simulation.runner import FTPSource
from simulation.runner import RogueSource


class ExperimentResults(object):
    """A container for the results of a single simulation.

    This object contains the scheduler which was used in the simulation, the
    total offered load of all the traffic sources during the simulation, and
    resulting pipeline statistics.

    The specific statistics for each source can be retrieved using
    dictionary-like key-based retrieval notation.

    """

    def __init__(self, scheduler, total_offered_load, run_number, stats):
        """Instantiates this object by simply stashing the given arguments.

        `scheduler` is a string specifying which scheduler was used (`'FIFO'`,
        `'RR'`, or `'DRR'`).

        `total_offered_load` is a float representing the total offered load of
        all traffic sources through the output link.

        `run_number` is the number of the trial for which these are the
        results.

        `stats` is a mapping from traffic source ID number (an integer) to the
        `simulation.analysis.PipelineStatistics` object which was produced
        after the simulation concluded.

        """
        self.scheduler = scheduler
        self.total_offered_load = total_offered_load
        self.run_number = run_number
        self.stats = stats

    def __getitem__(self, source_id):
        """Gets the `PipelineStatistics` object for the traffic source with the
        specified ID number.

        """
        return self.stats[source_id]


def _type_to_name(source_type):
    """Returns a human-readable string which represents the specified type of a
    traffic source.

    """
    if source_type == FTPSource:
        return 'ftp'
    if source_type == TelnetSource:
        return 'telnet'
    if source_type == RogueSource:
        return 'rogue'
    raise Exception('unrecognized source type {0}'.format(source_type))


def run_experiment((scheduler, total_offered_load, run_number), *args, **kw):
    """Runs a single experiment simulation with the specified scheduler (a
    string chosen from `'FIFO'`, `'RR'`, or `'DRR'`), and total offered load (a
    float).

    The `run_number` is the number of the trial.

    The three required arguments must be provided as a two-tuple.

    Returns the `ExperimentResults` object which results from running a
    simulation with the specified properties.

    The other positional and keyword arguments are passed on to the
    `simulation.runner.run_simulation` function.

    """
    result = run_simulation(scheduler=scheduler,
                            total_offered_load=total_offered_load, *args, **kw)
    return ExperimentResults(scheduler, total_offered_load, run_number, result)


def write_results(results_table, start_time, f=sys.stdout):
    """Writes the data from the table of results to the file-like object `f`.

    The output is a sequence of lines reqpresenting records from the specified
    table of results. The format of each line of the output (except for lines
    starting with an initial hash [#], which are comments) is

        <scheduler> <load> <source_id> <source_type> <run_number> \
          <measured_throughput> <throughput_difference> <throughput_ratio> \
          <mean_latency>

    `scheduler`, a string, is the identifier for the type of scheduler used
    during that simulation.

    `load`, a float, is the total offered load for all sources during that
    simulation.

    `source_id`, an integer, is the ID number of the traffic source that this
    record represents.

    `source_type` is a string representing the type of traffic source (`'ftp'`
    for FTP, `'telnet'` for telnet, and `'rogue'` for rogue).

    `run_number` is the number of the independent trial from which this
    measurement comes. 

    `measured_throughput`, the measured average throughput of this source over
    the entire time of the simulation, in bits per second.

    `throughput_difference`, a float, is the difference between the expected
    throughput and the measured throughput for this source, in bits per
    second. May be negative if the measured throughput was smaller than the
    expected throughput.

    `throughput_ratio`, a float, is the ratio of measured to expected
    throughput for this source. A value of one means that the measured
    throughput exactly equaled the expected throughput. A value less than one
    means the measured throughput was less than expected. A value greater than
    one means that the measured throughput was greater than expected.

    `mean_latency`, a float, is the mean latency for all packets sent by this
    source, in seconds.

    """
    f.write('# experiments started at {0}\n'.format(start_time))
    f.write('# written at {0}\n'.format(datetime.now().isoformat()))
    f.write('# scheduler load source_id source_type run_number'
            ' measured_throughput throughput_difference throughput_ratio'
            ' mean_latency\n')
    for scheduler in SCHEDULERS:
        for load in LOADS:
            for run in range(NUM_TRIALS):
                for source in range(NUM_SOURCES):
                    stats = results[scheduler][load][run][source]
                    f.write('{0} {1} {2} {3} {4} {5} {6} {7} {8}\n'
                            .format(scheduler, load / 10.0, source,
                                    _type_to_name(stats.source_type), run,
                                    stats.measured_throughput,
                                    stats.throughput_difference,
                                    stats.throughput_ratio,
                                    stats.mean_latency))


if __name__ == '__main__':
    start_time = datetime.now().isoformat()
    # create a list of all possible combinations of parameters; each element of
    # the list is of the form (scheduler, load, trial_number)
    parameters = list(itertools.product(SCHEDULERS, LOADS, range(NUM_TRIALS)))
    # create a pool of worker processes, but no more than the total number of
    # trials
    try:
        num_processes = cpu_count()
    except NotImplementedError:
        num_processes = 1
    pool = Pool(min(num_processes, len(parameters)))
    # split up the independent experiments among the worker processes
    temp_results = pool.map(run_experiment, parameters)
    # create a three-dimensional table to which to add the results; the table
    # is of the form results[scheduler][load][num_trial] = stats
    results = dict([(scheduler,
                     dict([(load,
                            dict([(num_trial, None)
                                  for num_trial in range(NUM_TRIALS)]))
                           for load in LOADS]))
                    for scheduler in SCHEDULERS])
    for p, r in zip(parameters, temp_results):
        results[p[0]][p[1]][p[2]] = r
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as f:
            write_results(results, start_time, f)
    else:
        write_results(results, start_time)
