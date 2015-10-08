# config.py - configuration for client.py
#
# Shuwen Sun
# Oct 2015


HOST = '128.197.11.36'
PORT = 58909  # test port
RECEIVE_BYTES = 4096
KB = lambda n: n * (2 ** 10)
RTT_SIZES = 1, 100, 200, 400, 800, 1000
TPUT_SIZES = [KB(2 ** k) for k in range(0, 6)]
NUM_PROBES = 10
NUM_TRIALS = 5
SERVER_DELAYS = [0, 0.5, 1]
MEASUREMENTS = dict(rtt=RTT_SIZES, tput=TPUT_SIZES)