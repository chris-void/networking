# CS655 TCP socket echo server #

This directory contains the CS655 TCP socket echo server.

This README file is written in the markup language "[Markdown][1]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
October 2011

[1]: http://daringfireball.net/projects/markdown

## Downloading ##

This package uses [Mercurial][2] for version control. It's main repository is
hosted on bitbucket at
[https://bitbucket.org/jfinkels/cs655][https://bitbucket.org/jfinkels/cs655].

To download this package:

    hg clone https://bitbucket.org/jfinkels/cs655

[2]: http://mercurial.selenic.com

## Dependencies ##

Running the server and client scripts requires [Python version 3.2][3].

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
install the Python header files on Ubuntu 11.04, for example, run:

    sudo apt-get install python-dev

If that doesn't work, you can install these libraries using your distribution's
package manager. For example, on Ubuntu 11.04:

   sudo apt-get install python2.7 python-numpy python-matplotlib

[3]: http://www.python.org/download/releases/3.2
[4]: http://www.python.org/download/releases/2.7
[5]: http://matplotlib.sourceforge.net
[6]: http://www.numpy.org
[7]: http://www.virtualenv.org

## Contents ##

This directory contains:

* `client.py` - the Python script which runs the client side of the specific
  experiments described in the assignment
* `config.py` - some constants common to both the `client.py` script and the
  `plot.py` script
* `experiment.py` - module providing a class which encapsulates a single trial
  of the experiment with a specific set of parameters
* `plot.py` - the Python script which generates the plots for the data measured
  from the experiments run by the `client.py` script
* `README.md` - this file
* `REPORT.md` - the results report for the experiments
* `run-tests.sh` - script which runs the unit tests for this package
* `server.py` - the Python script which runs the server for the protocol
  specified in the assignment
* `tests/` - the unit tests for the `simulation` package

## Testing ##

To run the unit tests for this package run the `run-tests.sh` script in this
directory:

    ./run-tests.sh

You can also run specific tests by doing, for example:

    python -m unittest tests.test_server.MeasurementProtocolHandlerTest

## Running ##

To run the server for the protocol specified in the assignment, run the
following command:

    ./server.py $PORT

where `$PORT` is the number of the port of the socket on which the server
should listen for connections. To get debug messages, add a terminal `debug`
argument:

    ./server.py $PORT debug

To run the client, which runs all the experiments described in the assignment,
run the following command:

    ./client.py $HOST $PORT

where `$HOST` is the name of the host on which the server is running, and
`$PORT` is the number of the port on which the server is running. To get debug
messages, add a terminal `debug` argument:

    ./client.py $HOST $PORT debug

This script writes a table of results to `stdout`. To capture the results in a
file, redirect the output to a file:

    ./client.py $HOST $PORT > results.out

To generate plots from the `results.out` file created by the `client.py`
script, run the `plot.py` script, like this:

    ./plot.py results.out

If no file is specified as a command-line argument, results will be read from
`stdin`. The output will be written to the directory `output/{datetime}`, where
`{datetime}` is the current date and time in `YY-MM-DD-HH-MM-SS` format. In
this directory, `plot.py` will write, for each server delay value, one plot for
round-trip time as it depends on message size and one plot for throughput as it
depends on message size.

## Contact ##

Jeffrey Finkelstein <jeffreyf@bu.edu>
