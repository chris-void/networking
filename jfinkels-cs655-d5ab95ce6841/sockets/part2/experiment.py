# experiment.py - an experiment with a specific set of parameters
#
# CS655 sockets assignment
# Jeffrey Finkelstein
# October 2011
"""Provides a class which encapsulates a single trial of the experiment
specified in the assignment with a specified set of parameters.

"""
from datetime import datetime
import logging
import socket

RECEIVE_BYTES = 4096
"""The maximum number of bytes to read when receiving a message from the
server over the socket.

"""


class ServerException(Exception):
    """Raised when the client recieves an error message from the server."""

    def __init__(self, message):
        """Stores the specified `message` as the human-readable description of
        this exception.

        """
        self.message = message

    def __str__(self):
        """Returns the human-readable description of this exception as
        specified in the constructor of this class.

        """
        return repr(self.message)


class Statistics(object):
    """A pair of times, representing the time at which a message was sent and
    the time at which the message was received, along with the size of the
    message.

    """

    def __init__(self, send_time, recv_time, message_size):
        """Stores the send and receive times of a message, along with its size
        in bytes.

        """
        self.send_time = send_time
        self.recv_time = recv_time
        self.message_size = message_size

    def round_trip_time(self):
        """Returns the total number of seconds between the time that the
        message was received and the time that it was sent, as specified in the
        constructor of this class.

        """
        return (self.recv_time - self.send_time).total_seconds()

    def throughput(self):
        """Returns the throughput, in bits per second, of the round-trip of the
        message.

        """
        return self.message_size / self.round_trip_time()


class Experiment(object):
    """Encapsulates an individual trial with a specified set of parameters.

    Creates a socket using the `socket.socket` function at the time of
    instantiation, but does not connect to it. This class is intended to be
    used as a context manager in a `with` statement, so the socket is connected
    on entering the context, and closed on exiting the context.

    Once inside the `with` statement, use the `run()` function to run the
    experiment with the parameters specified in the constructor of this class.

    After running the experiment with the `run()` function, the `times`
    attribute contains a list of `TimePair` objects which represent the times
    at which each of the messages was sent and received, in order.

    """


    def __init__(self, host, port, measurement_type, num_probes, message_size,
                 delay):
        """Creates (but does not connect to) a socket at the specified host and
        port number, and stores the experiment parameters for later use when
        the `run()` function is called.

        `host` and `port` comprise the IP address of the server to which to
        connect. `port` must be an integer.

        `measurement_type` can be either the string `'rtt'` (for round-trip
        time) or the string `'tput'` (for throughput).

        `num_probes` is an integer specifying the number of probe messages to
        send when performing the experiment.

        `message_size` is the number of bytes in each probe message.

        `delay` is the amount of delay, in milliseconds, which we will instruct
        the server to inject between each probe message.

        """
        self.host, self.port = host, port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.measurement_type = measurement_type
        self.max_probes = num_probes
        self.message_size = message_size
        self.delay = delay
        self.stats = []

    def __enter__(self):
        """Connects the socket specified by the address given in the
        constructor of this class, and returns this object.

        """
        self.sock.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the socket connection created on entering the context.

        The parameters are ignored.

        """
        self.sock.close()

    def check_for_error(self, data):
        """Raises a `ServerException` if the specified `data`, a `bytes` object
        which is the response from the server, starts with the bytes `b'404
        ERROR'`.

        """
        if data.startswith(b'404 ERROR'):
            raise ServerException(data[11:])

    def request_bytes(self, *args, suffix=b'', **kw):
        """Joins the positional arguments (which must all be strings) with
        spaces, appends the specified suffix (which must be a `bytes` object),
        and appends a newline character.

        Returns a `bytes` object suitable for sending to the server.

        """
        if suffix:
            suffix = b' ' + suffix
        return ' '.join(args).encode('utf8') + suffix + b'\n'

    def run(self):
        """Runs the experiment with the parameters specified in the constructor
        of this class.

        If at any point the server responds with an error, this function will
        raise a `ServerException`.

        """
        self.send_setup_connection()
        self.send_probes()
        self.send_termination()

    def send_and_recv(self, message):
        """Sends the specified `message`, which must be a `bytes` object, and
        returns the next `RECEIVE_BYTES` bytes received from the server.

        """
        logging.debug('sending {}'.format(message))
        self.sock.send(message)
        result = self.sock.recv(RECEIVE_BYTES)
        logging.debug('receive {}'.format(result))
        return result

    def send_probes(self):
        """Repeatedly sends probe messages to the server and records
        statistics.

        The number and size of the messages is specified in the constructor of
        this class.

        If the server responds with an error, this function will raise a
        `ServerException`.

        """
        logging.debug('sending probes...')
        for n in range(1, self.max_probes + 1):
            logging.debug('  probe {}'.format(n))
            data = self.request_bytes('m', str(n),
                                      suffix=b'.' * self.message_size)
            time_sent = datetime.now()
            self.sock.send(data)
            received = self.sock.recv(RECEIVE_BYTES)
            while len(received) < self.message_size:
                received += self.sock.recv(RECEIVE_BYTES)
                logging.debug('want {} bytes, got {} bytes'
                              .format(self.message_size, len(received)))
            time_received = datetime.now()
            self.check_for_error(received)
            # This is not very accurate; there is some overhead incurred for
            # function calls, assignments, etc. for which we do not account.
            result = Statistics(time_sent, time_received, self.message_size)
            self.stats.append(result)

    def send_setup_connection(self):
        """Sends the setup connection message to the server according to the
        protocol specified in the assignment.

        If the server responds with an error, this function will raise a
        `ServerException`.

        """
        data = self.request_bytes('s', self.measurement_type,
                                  str(self.max_probes), str(self.message_size),
                                  str(self.delay))
        result = self.send_and_recv(data)
        self.check_for_error(result)

    def send_termination(self):
        """Sends the connection termination message to the server according to
        the protocol specified in the assignment.

        If the server responds with an error, this function will raise a
        `ServerException`.

        """
        result = self.send_and_recv(b't \n')
        self.check_for_error(result)
