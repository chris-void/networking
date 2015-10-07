# CS655 error control simulation #

This directory contains the CS655 TCP reliable data transfer/error control simulation.

This README file is written in the markup language "[Markdown][1]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
November 2011

[1]: http://daringfireball.net/projects/markdown

## Downloading ##

This package uses [Mercurial][2] for version control. It's main repository is
hosted on bitbucket at
[https://bitbucket.org/jfinkels/cs655][https://bitbucket.org/jfinkels/cs655].

To download this package:

    hg clone https://bitbucket.org/jfinkels/cs655

[2]: http://mercurial.selenic.com

## Dependencies ##

Running the simulation requires [Python version 3.2][3].

Plotting the results of the simulations requires [Python version 2.7][4] and
the following Python libraries:

* [matplotlib][5]
* [NumPy][6]

Using `pip` is probably the easiest way to install these. I recommend using
[virtualenv][7] to create a virtual Python development environment in a folder
(called, for example, `env/`), then installing the dependencies (after
installing Python 2.7):

    # create a virtual Python 2.7 development environment in the directory env/
    virtualenv -p python2.7 env

    # activate the virtual environment in your current shell
    source env/bin/activate
    
    # install the dependencies in the virtual environment
    pip install numpy matplotlib

If `numpy` fails to install, it is probably because it requires compiling C
code into modules usable by Python, so the Python header files are required. To
install the Python header files on Ubuntu 11.10, for example, run:

    sudo apt-get install python-dev

If that doesn't work, you can install these libraries using your distribution's
package manager. For example, on Ubuntu 11.10:

   sudo apt-get install python2.7 python-numpy python-matplotlib

[3]: http://www.python.org/download/releases/3.2
[4]: http://www.python.org/download/releases/2.7
[5]: http://matplotlib.sourceforge.net
[6]: http://www.numpy.org
[7]: http://www.virtualenv.org

## Contents ##

This directory contains:

* `config.py` - some constants common to both the `experiments.py` script and
  the `plot.py` script
* `DESIGN.md` - a document explaining the high-level design of the experiments
* `experiments.py` - the Python script which runs the specific experiments
  described in the assignment and outputs the data
* `plot.py` - the Python script which generates the plots for the data measured
  from the experiments run by the `experiments.py` script
* `README.md` - this file
* `REPORT.md` - the results report for the experiments
* `runonce.py` - script which performs a single run of the simulation with a
  specific set of parameters
* `run-tests.sh` - script which runs the unit tests for the `simulation` package
* `simulation/` - the Python code which allows running a simulation and
  collecting statistics; this is a Python package, so you can import it in
  Python:

      >>> import simulation

* `tests/` - the unit tests for the `simulation` package

## Testing ##

To run the unit tests for this package run the `run-tests.sh` script in this
directory:

    ./run-tests.sh

You can also run specific tests by doing, for example:

    python3 -m unittest tests.test_endpoints.test_gobackn

## Running ##

To run the experiments specified in the assignment, run the following command:

    python3 experiments.py results.out

A table of results will be written to the file `results.out`. If no file is
specified as a command-line argument, results will be written to `stdout`.

To generate plots from the `results.out` file created by the `experiments.py`
script, run the `plot.py` script, like this:

    python2.7 plot.py results.out

If no file is specified as a command-line argument, results will be read from
`stdin`. The output will be written to the directory `output/{datetime}`, where
`{datetime}` is the current date and time in `YY-MM-DD-HH-MM-SS` format. In
this directory, `plot.py` will write one plot, `rtts.png`, which is a plot of
average packet round-trip time as it depends on both corruption probability
and loss probability.

You can also perform a single run of the simulation with a specific set of
parameters by running the `runonce.py` script:

    python3 runonce.py

However, I haven't tested this much.

There are a bunch of commmand-line parameters. To view usage information, run
the command:

    python3 runonce.py -h

## Contact ##

Jeffrey Finkelstein <jeffreyf@bu.edu>
