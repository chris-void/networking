# CS655 homework 2 #

Jeffrey Finkelstein
17 October 2011

1. (P7) The total time required to get the IP address for the associated URL is

       T1 = RTT1 + RTT2 + ... + RTT8

   The total time required to lookup the IP address and get the HTML is

       T = T1 + RTT0

   (P10) With parallel downloads over ten parallel instances of non-persistent
   HTTP to download ten packets of length 100,000 bits, the total time required
   is

       3 * (200 bits / 15 bps) + (100000 bits / 15 bps)
       = 3 * (40 / 3) seconds + 6666 seconds
       = 6706 seconds

   The first term is the three delays due to TCP handshaking and the HTTP GET
   request. Since there are ten parallel connections, the throughput is one
   tenth of 150 bps, which is 15 bps.

   If a single instance of persistent HTTP were used to download the ten
   objects instead, the total delay would be

       3 * (200 bits / 150 bps) + 10 * (100000 bits / 150 bps)
       = 3 * (4 / 3) seconds + 6666 seconds
       = 6670 seconds

   Hence a single instance of persistent HTTP is faster by about 30
   seconds. However, the overall delay is on the order of hours, so this would
   not be noticeable in practice.

   (P22) Following the formulae on pages 148 and 149 for minimum distribution
   time for client/server model and peer to peer model, we get the following
   values:
   
       Minimum distribution time for client/server model

                      peer upload speed

                || 300 KBps | 700 Kbps |  2 Mbps  |
           =====++==========+==========+==========+
             10 ||   7500 s |   7500 s |   7500 s |
           -----++----------+----------+----------+
        N   100 ||  50000 s |  50000 s |  50000 s |
           -----++----------+----------+----------+
           1000 || 500000 s | 500000 s | 500000 s |
           -----++----------+----------+----------+

   
       Minimum distribution time for peer-to-peer model

                      peer upload speed

                || 300 KBps | 700 Kbps | 2 Mbps  |
           =====++==========+==========+=========+
             10 ||   7500 s |   7500 s |  7500 s |
           -----++----------+----------+---------+
        N   100 ||  25000 s |  15000 s |  7500 s |
           -----++----------+----------+---------+
           1000 ||  45454 s |  20547 s |  7500 s |
           -----++----------+----------+---------+

   (P25) Physical routers are not considered part of an "overlay network", so
   the total number of vertices in the overlay graph is `N` and the number of
   edges is `N * (N - 1) / 2`.

   (P33) Assigning uniformly random identifiers to newly joined peers will
   cause a discrepancy between overlay distances and physical distances,
   assuming the distributed hash table is distributed across a wide physical
   area. This is because the identifier is independent of the physical
   location. The distributed hash table would see a decrease in performance,
   because queries to successors which are physically distant will cause a
   greater delay.

2. (P6) Suppose the sender is in state "wait for ACK or NAK 1" and the receiver
   is in state "wait for 0 from below". If the sender is sending packet 1, the
   receiver will respond with NAK 0. When the sender receives NAK 0, it will
   resend packet 1. This cycle repeats, and is a deadlock.

   (P12) If messages can be reordered while in transit, then the following
   situation will cause a problem:
   
            sender           receiver
              |..               |
              |  ..             |
              |    .. P0 ..     |
              |            ..   |
              |              ..>|
       timeout|..             **|
              |  P0        ACK0 |
              |    ..    **     |
              |      .***       |
              |    **  ..       |
              |  **      .      |
              |<*        .      |
              |....      .      |
              |    ..P1........>|
              |          .      |
              |        **.******|
              |<*ACK1**  .      |
              |           ..    |
              |             ...>|
              |...P2...         |
              |        ........>|
              V                 V

   In this situation, the sender sends two copies of P0 due to timeout, while
   the ACK0 is being sent back to it. The second copy of P0 gets delayed in
   transit while the sender successfully transmits (and gets an ACK for)
   P1. Now the receiver gets the delayed P0, which has the expected sequence
   number (zero) even though the receiver *should* be receiving P2 (which also
   has sequence number zero).

   (P18) For this question, I assume that the receiver, host C, is able to
   identify the source channel of the incoming segments (that is, whether the
   segment originates from host A or host B). The finite state automata for
   hosts A and B are the same as the sender finite state automaton in the
   reliable data transfer protocol described in the textbook, `rdt3.0`. The
   finite state automaton for the receiver, host C is given in the attached
   sheet.

   (P20) The finite state automata for the protocol are as follows. First for
   the sender, A:

   * state "wait for request" (the start state):
     - on request from layer above:
       + start countdown timer
       + send request R
       + move to state "wait for response"
   * state "wait for response":
     - on timeout:
       + reset countdown timer
       + resend request R
       + remain in this state
     - on receipt of data D:
       + deliver data D to the layer above
       + move to state "wait for request"

   Next for the receiver, B:

   * state "wait for request":
     - on receipt of request R:
       + send response D
       + remain in this state

3. (a) Consider the following situation:

            sender           receiver
              |..               |
              |  ..             |
              |    ..P0,0..     |
              |            ..   |
              |              ..>|
       timeout|..             **|
              | P0,1       ACK  |
              |    ..    **     |
              |      .***       |
              |    **  ..       |
              |  **      ...    |
              |<*           ...>|
       dropped|..P1,0..X      **|
              |             **  |
              |           **    |
              |        **       |
              |<*ACK**          |
              |..               |
              |  ..             |
              |    P2,0........>|
              |                 |
              V                 V

   In this situation, the sender receives an ACK for 0 intended to inform it to
   transmit P1, but it is regarded as an ACK for P1, which is dropped. This
   means the receiver never receives P1, as the sender just moves on to sending
   P2.

   (b) I don't know.

4. Let L = 1000 bits per packet, R = 1000000 bits per second, and RTT = 2 *
   0.27 seconds = 0.54 seconds. Then the utilization of the sender, U, in a
   stop-and-wait protocol is

       U = (L / R) / (RTT + (L / R))
         = (1000 / 1000000) / ((54 / 100) + (1000 / 1000000))
         = (1 / 1000) / (541 / 1000)
         = 1 / 541
         = 1.848 * (10 ^ -3)

   For a go-back N protocol with 3-bit sequence numbers, the utilization is

       U = ((2 ^ 3) * (L / R)) / (RTT + (L / R))
         = (8 / 1000) / (541 / 1000)
         = 8 / 541
         = 1.479 * (10 ^ -2)

   Therefore we conclude that in this situation, go-back N has better
   utilization.

5. First we compute the round-trip time for bits in this channel.

       distance = rate * time
       time = distance / rate
       RTT / 2 = 3000 km / (1 km / 6 microsec)
       RTT = 6000 * 6 microsec
           = 36000 microsec
           = 36 milliseconds
           = 0.036 seconds

   Next we compute the number of packets needed for perfect utilization of the
   channel. Suppose L = 64 * 8 bits = 512 bits, R = 1.5 * (10 ^ 6) bps, and let
   N be the number of packets.

       U = (N * L / R) / (RTT + (L / R))
       1 = (N * 512 / (1.5 * (10 ^ 6))) / (.036 + (512 / (1.5 * (10 ^ 6))))
         [after some algebra...]
       N = (3.6 * 1.5 / 5.12) * (10 ^ 2) + 1
         = 106.46

   The optimum number of packets is 106.46, but this is not a whole number. The
   nearest whole numbers are 106 and 107. The utilization at N = 107 would be
   greater than one, which is impossible, so we would choose N = 106, in which
   the utilization is 0.996. To count to 106 we would need 7 bits (since 2 ^ 7
   is 128).

   If we require that the number of packets be a power of two, then we would
   choose N = 64, and the number of bits would be 6. In this case, the
   utilization would be 0.601.
