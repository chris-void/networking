# CS655 routing simulation #

This directory contains the CS655 routing protocol simulation.

This README file is written in the markup language "[Markdown][1]".

Jeffrey Finkelstein <jeffreyf@bu.edu>
November 2011

[1]: http://daringfireball.net/projects/markdown

## Downloading ##

This package uses [Mercurial][2] for version control. Its main repository is
hosted on bitbucket at
[https://bitbucket.org/jfinkels/cs655][https://bitbucket.org/jfinkels/cs655].

To download this package:

    hg clone https://bitbucket.org/jfinkels/cs655

[2]: http://mercurial.selenic.com

## Dependencies ##

Running the simulation requires [Python version 3.2][3].

[3]: http://www.python.org/download/releases/3.2

## Contents ##

This directory contains:

* `README.md` - this file
* `runonce.py` - script which performs a single run of the simulation with a
  specific set of parameters
* `run-tests.sh` - script which runs the unit tests for the `routing` package
* `routing/` - the Python code which allows running a routing simulation; this
  is a Python package, so you can import it in Python:

      >>> import routing

* `tests/` - the unit tests for the `routing` package

## Testing ##

To run the unit tests for this package run the `run-tests.sh` script in this
directory:

    ./run-tests.sh

You can also run specific tests by doing, for example:

    python3 -m unittest tests.test_protocols.test_bases

## Running ##

You can perform a single run of the simulation with a specific set of
parameters by running the `runonce.py` script:

    python3 runonce.py

There are a bunch of commmand-line parameters. To view usage information, run
the command:

    python3 runonce.py -h

## Contact ##

Jeffrey Finkelstein <jeffreyf@bu.edu>
