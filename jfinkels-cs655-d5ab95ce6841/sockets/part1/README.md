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

[3]: http://www.python.org/download/releases/3.2

## Contents ##

This directory contains:

* `client.py` - the Python script which sends a message to a server
* `README.md` - this file
* `server.py` - the Python script which echos messages over TCP

## Running ##

To run the echo server, run the following command:

    ./server.py $PORT

where `$PORT` is the number of the port of the socket on which the server
should listen for connections.

To run the client which sends a single message to the server, run the following
command:

    ./client.py $HOST $PORT $MESSAGE

where `$HOST` is the name of the host on which the server is running, `$PORT`
is the number of the port on which the server is running, and `$MESSAGE` is the
message to send to the server. Everything after the port number is considered
to be the message to send to the server.

## Contact ##

Jeffrey Finkelstein <jeffreyf@bu.edu>
