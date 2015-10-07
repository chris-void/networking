# CS655 scheduler simulation #

This directory contains the CS655 packet traffic simulation.

This README file is written in the markup language "[Markdown][4]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
October 2011

[4]: http://daringfireball.net/projects/markdown

## Downloading ##

This package uses [Mercurial][7] for version control. It's main repository is
hosted on bitbucket at
[https://bitbucket.org/jfinkels/cs655][https://bitbucket.org/jfinkels/cs655].

To download this package:

    hg clone https://bitbucket.org/jfinkels/cs655

[7]: http://mercurial.selenic.com

## Dependencies ##

This application requires [Python version 2.7][1].

Running the simulations requires the following Python library:

* [SimPy][2]
* [NumPy][6]

Plotting the results of the simulations requires the following Python
library:

* [matplotlib][5]
* [NumPy][6]

Using `pip` or `easy_install` is probably the easiest way to install these. I
recommend using [virtualenv][3] to create a virtual Python development
environment in a folder (called, for example, `env/`), then installing the
dependencies (after installing Python 2.7):

    # create a virtual Python 2.7 development environment in the directory env/
    virtualenv -p python2.7 env

    # activate the virtual environment in your current shell
    source env/bin/activate
    
    # install the dependencies in the virtual environment
    pip install simpy numpy matplotlib

If `numpy` fails to install, it is probably because it requires compiling C
code into modules usable by Python, so the Python header files are required. To
install the Python header files on Ubuntu 11.04, for example, run:

    sudo apt-get install python-dev

If that doesn't work, you can install these libraries using your distribution's
package manager. For example, on Ubuntu 11.04:

   sudo apt-get install python2.7 python-simpy python-numpy python-matplotlib

[1]: http://www.python.org/download/releases/2.7
[2]: http://simpy.sourceforge.net
[3]: http://www.virtualenv.org
[5]: http://matplotlib.sourceforge.net
[6]: http://www.numpy.org

## Contents ##

This directory contains:

* `config.py` - some constants common to both the `experiments.py` script and
  the `plot.py` script
* `DESIGN.md` - a document explaining the high-level design of the experiments
* `experiments.py` - the Python script which runs the specific experiments
  described in the assignment
* `plots.py` - the Python script which generates the plots for the data
  measured from the experiments run by the `experiments.py` script
* `README.md` - this file
* `REPORT.md` - the results report for the experiments
* `run-tests.sh` - script which runs the unit tests for this package
* `simulation/` - the Python code which allows running a simulation and
  collecting statistics; this is a Python package, so you can import it in
  Python:

      >>> import simulation

  It can also be executed as the main module in a Python script:
  
      python simulation -c FIFO -m 0.4

* `tests/` - the unit tests for the `simulation` package

## Testing ##

To run the unit tests for this package run the `run-tests.sh` script in this
directory:

    ./run-tests.sh

You can also run specific tests by doing, for example:

    python -m unittest tests.test_schedulers.RoundRobinTest

## Running ##

To run the experiments specified in the assignment, run the following command:

    python experiments.py results.out

A table of results will be written to the file `results.out`. If no file is
specified as a command-line argument, results will be written to `stdout`.

To generate plots from the `results.out` file created by the `experiments.py`
script, run the `plot.py` script, like this:

    python plot.py results.out

If no file is specified as a command-line argument, results will be read from
`stdin`. The output will be written to the directory `output/{datetime}`, where
`{datetime}` is the current date and time in `YY-MM-DD-HH-MM-SS` format. In
this directory, `plot.py` will write two plots for each traffic source--one for
mean throughput deficit for each scheduler as it depends on total offered load,
and one for mean packet latency for each scheduler as it depends on total
offered load.

You can also perform a single run of the simulation with a specific set of
parameters by running the `simulation` package as the main module:

    python simulation -c FIFO -m 0.4

Those are the two required parameters, but there are others. To view usage
information, run the command:

    python simulation --help

## Contact ##

Jeffrey Finkelstein <jeffreyf@bu.edu>
