# CS655 assignment 4 #

Jeffrey Finkelstein
6 December 2011

1. (a) Each segment sends 1000 bytes, and after each ACK the window size is
  increased by one segment. Therefore the window size is initially 1, then
  increases to 2 after the first ACK, then 4 after receiving the next two ACKs,
  then 8 after receiving the next 4 ACKS, etc. After one round-trip time we
  have sent 2^0 kilobytes, after two round-trip times we have sent 2^0 + 2^1,
  etc. These are also the window sizes. We want to know when the window reaches
  1 Megabyte, or 1000 Kilobytes, which is 1000 segments. So we want to find N
  such that (1 + 2 + ... + 2^(N - 1)) >= 1000. Thus the value of N is 10.

  (b) After the sender's congestion window size becomes 1 MB, it cannot send
  any more than 1 MB worth of segments at a time, since it *knows* that the
  receiver cannot accept more than that at a time (because it is advertised).
  After the first 10 round trip times the sender's congestion window is 1 MB
  and 1 MB of the file has been sent. At this point the sender continues by
  sending 1 MB at a time. Thus after 9 more round trip times, the entire 10 MB
  file has been sent. The total number of round-trip times is 10 + 9 = 19.

  (c) The time to send the file is 19 * 110ms = 2090ms = 2.09 seconds. The
  effective throughput of the transfer is the number of bytes sent over time,
  which is 10 * (10 ^ 6) bytes / 2.09 seconds = 4784689 bytes per second, which
  is 38277511 bits per second, or 38.28 Megabits per second. The channel
  capacity is 1 Gbps = 1000 Mbps, so the utilization of the channel capacity is
  3.83 percent.

2. ISP C may use the "metric" attribute, also known as the "multi-exit
  discriminator" attribute to provide a hint to ISP B as to which entry point
  into ISP C to prefer. ISP C would advertise a lower metric value for the east
  coast router than the west coast router to ISP B, so that ISP B prefers the
  east coast router.

3. B waits for 1 * 512 bit times after the jam signal has completed
  transmission, then must wait the 96 bit times for an idle channel, so the
  retransmission occurs at 293 + 512 + 96 = 901 bit times. A waits for 0 * 512
  bit times after the jam signal has completed transmission, then must wait the
  96 bit times for an idle channel, so the retransmission occurs at 293 + 0 +
  96 = 389 bit times. Since the propagation delay is 245 bit times, A's
  transmission arrives at B at 389 + 0 + 245 = 634 bit times. Since B has
  scheduled its transmission at time 901, it will refrain from transmitting at
  its scheduled time if A is sending more than (901 - 96) - 634 = 171 bits.
