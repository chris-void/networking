# config.py - commong configuration
#
# CS655 sockets assignment
# Jeffrey Finkelstein
# October 2011
KB = lambda n: n * (2 ** 10)
"""Returns 1024 times the input."""
RTT_SIZES = 1, 100, 200, 400, 800, 1000
"""Test message sizes (in bytes) for the round-trip times test."""
TPUT_SIZES = [KB(2 ** k) for k in range(0, 6)]
"""Test message sizes (in bytes) for the throughput times test."""
NUM_PROBES = 10
"""The number of probes per message size to send to the server."""
NUM_TRIALS = 5
"""The number of independent trials of each experiment with a specific set of
parameters to perform.

"""
SERVER_DELAYS = [0, 0.5, 1]
"""The time in seconds that the server should wait before echoing the payload
of measurement probes.

"""
MEASUREMENTS = dict(rtt=RTT_SIZES, tput=TPUT_SIZES)
"""A dictionary mapping identifying strings for measurement types to lists of
message sizes to use in the experiments corresponding to those measurement
types.

"""
