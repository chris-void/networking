# test_server.py - unit tests for the server module
#
# CS655 simulation assignment
# Jeffrey Finkelstein
# October 2011
"""Unit tests for the server module."""
import socket
import socketserver
import subprocess
import threading
from unittest import TestCase

from server import MeasurementProtocolHandler as MPH

__all__ = ['MeasurementProtocolHandlerTest']


RECEIVE_BYTES = 4096
"""The number of bytes to receive when reading from a socket."""
HOST, PORT = 'localhost', 9999
"""The host and port at which the server will be created in these tests."""


class TestServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """TCP Server which starts a new thread for each incoming connection, and
    allows reusing the same address for a socket.

    """
    allow_reuse_address = True


class MeasurementProtocolHandlerTest(TestCase):
    """Unit tests for the MeasurementProtocolHandler class."""

    def setUp(self):
        """Creates the server and client and starts the server in a new thread.

        """
        self.server = TestServer((HOST, PORT), MPH)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.setDaemon(True)
        self.server_thread.start()

    def tearDown(self):
        """Closes the client connection and shuts down the server."""
        self.server.shutdown()

    def request(self, data, encoding='UTF-8'):
        """Encodes the requested `data` as a byte string in the specified
        `encoding`, sends it to the test server via a new client socket
        connection, receives `RECEIVE_BYTES` bytes of response from the
        server, then closes the connection.

        """
        with socket.create_connection((HOST, PORT)) as sock:
            sock.send(data.encode(encoding))
            result = sock.recv(RECEIVE_BYTES)
        return result

    def as_request_string(self, *args, **kw):
        """Returns the string consisting of each of the positional arguments
        with spaces between them and a terminal newline character.

        """
        return ' '.join(args) + '\n'

    def as_request_bytes(self, *args, **kw):
        """Returns the result of calling `as_request_string` with the given
        positional and keyword arguments encoded using UTF-8 into a bytes
        object.

        """
        return self.as_request_string(*args, **kw).encode('utf8')

    def test_invalid_protocol_phase_identifier(self):
        """Tests that a request with an invalid protocol phase identifier
        produces an error response.

        """
        request_data = self.as_request_string('x')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Protocol Phase Identifier', data)

    def test_setup(self):
        """Test for the connection setup phase."""
        request_data = self.as_request_string('s', 'rtt', '10', '1024', '1000')
        data = self.request(request_data)
        self.assertEqual(b'200 OK: Ready', data)

        request_data = self.as_request_string('s', 'tput', '1', '512', '400')
        data = self.request(request_data)
        self.assertEqual(b'200 OK: Ready', data)

        request_data = self.as_request_string('s', 'xxx', '10', '1024', '1000')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Connection Setup Message', data)

        request_data = self.as_request_string('s', 'rtt', 'xx', '1024', '1000')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Connection Setup Message', data)

        request_data = self.as_request_string('s', 'rtt', '10', 'xxxx', '1000')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Connection Setup Message', data)

        request_data = self.as_request_string('s', 'rtt', '10', '1024', 'xxxx')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Connection Setup Message', data)

        request_data = self.as_request_string('s', 'too', 'few', 'args')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Connection Setup Message', data)

        request_data = self.as_request_string('s', 'too', 'few', 'args')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Connection Setup Message', data)

        request_data = self.as_request_string('s', 'too', 'too', 'too', 'many',
                                              'args')
        data = self.request(request_data)
        self.assertEqual(b'404 ERROR: Invalid Connection Setup Message', data)

    def test_measurement(self):
        """Test for the measurement phase."""
        with socket.create_connection((HOST, PORT)) as sock:
            request_data = self.as_request_bytes('s', 'rtt', '3', '4', '0')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'200 OK: Ready', data)

            request_data = self.as_request_bytes('m', '1', '.' * 4)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'.' * 4, data)

            request_data = self.as_request_bytes('m', '2', '.' * 4)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'.' * 4, data)

            request_data = self.as_request_bytes('m', '3', '.' * 4)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'.' * 4, data)

            request_data = self.as_request_bytes('m', '4', '.' * 4)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'404 ERROR: Invalid Measurement Message', data)

        with socket.create_connection((HOST, PORT)) as sock:
            request_data = self.as_request_bytes('s', 'rtt', '3', '4', '0')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'200 OK: Ready', data)

            request_data = self.as_request_bytes('m', '2', '.' * 4)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'404 ERROR: Invalid Measurement Message', data)

        with socket.create_connection((HOST, PORT)) as sock:
            request_data = self.as_request_bytes('s', 'rtt', '3', '4', '0')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'200 OK: Ready', data)

            request_data = self.as_request_bytes('m', '1', '.' * 3)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'404 ERROR: Invalid Measurement Message', data)

        with socket.create_connection((HOST, PORT)) as sock:
            request_data = self.as_request_bytes('s', 'rtt', '3', '4', '0')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'200 OK: Ready', data)

            request_data = self.as_request_bytes('m', '1')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'404 ERROR: Invalid Measurement Message', data)

    def test_termination(self):
        """Tests that the server responds to the termination message as
        expected.

        """
        with socket.create_connection((HOST, PORT)) as sock:
            request_data = self.as_request_bytes('s', 'rtt', '1', '4', '0')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'200 OK: Ready', data)

            request_data = self.as_request_bytes('m', '1', '.' * 4)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'.' * 4, data)

            request_data = self.as_request_bytes('t', ' ')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'200 OK: Closing Connection', data)

        with socket.create_connection((HOST, PORT)) as sock:
            request_data = self.as_request_bytes('s', 'rtt', '1', '4', '0')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'200 OK: Ready', data)

            request_data = self.as_request_bytes('m', '1', '.' * 4)
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'.' * 4, data)

            request_data = self.as_request_bytes('t', 'too', 'many', 'args')
            sock.send(request_data)
            data = sock.recv(RECEIVE_BYTES)
            self.assertEqual(b'404 ERROR: Invalid Connection Termination'
                             b' Message', data)
