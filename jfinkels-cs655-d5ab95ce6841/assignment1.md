# CS655 assignment 1 #

Jeffrey Finkelstein
22 September 2011

1. On page 9 of the textbook, Kurose and Ross state,

   > A protocol defines the format and order of messages exchanged between two
   > or more communicating entities, as well as the actions taken on the
   > transmission and/or receipt of a message or other event.

   A network protocol is a protocol designed for use by computers which can
   communicate with one another.

   A network service is a system which facilitates access to applications
   running on hosts in a network.

   A service interface defines how external processes can interact with the
   service (for example, by specifying inputs and outputs). There may be
   several ways to implement such an interface, but the external process does
   not need to know the details of the implementation; it relies only on the
   interface to interact with the service.

   In a layered network architecture, the specification of each layer defines
   its interface to the layer above. A layer uses the services provided by the
   layer below it, in order to implement the interface it must expose to the
   layer above. Each layer communicates with the corresponding layer of a
   different host by following the rules of a specified protocol.

2. Round-trip times to various hosts at various times of day after 20 pings,
   starting from host `grubnick.bu.edu`.

      +==============+=============+============================+
      |              |             |   average round-trip time  |
      |     host     | time of day |  (min/avg/max/mdev, in ms) |
      +==============+=============+============================+
      |              |    20:45    |   0.217/0.220/0.232/0.016  |
      |  lug.bu.edu  |    17:51    |   0.220/1.435/6.482/1.999  |
      |              |    12:38    |   0.221/0.243/0.504/0.061  |
      +--------------+-------------+----------------------------+
      |              |    21:05    |   2.906/3.456/4.030/0.414  |
      | cs.umass.edu |    17:52    |   2.894/3.219/4.592/0.486  |
      |              |    12:38    |   2.929/3.634/5.002/0.766  |
      +--------------+-------------+----------------------------+
      |              |    21:06    | 12.109/12.300/13.352/0.284 |
      |   google.cn  |    17:53    | 12.846/12.969/13.160/0.114 |
      |              |    12:38    | 12.896/12.996/13.079/0.160 |
      +--------------+-------------+----------------------------+

3. The total nodal delay is the sum of nodal processing delay, queuing delay,
   transmission delay, and propagation delay. In this case, the nodal
   processing delay (to convert the 64 kbps bitstream into a 56 byte packet) is
   56 bytes * 8 bits per byte / 64000 bits per second = 0.007 seconds = 7
   milliseconds. There is no queuing delay. The transmission delay for this
   node is 56 bytes * 8 bits per byte / 2000000 bits per second = 0.000224
   seconds = 0.224 milliseconds. The propagation delay is 10 milliseconds. The
   total nodal delay is (7 + 0.224 + 10) milliseconds = 17.224
   milliseconds. Once this 56 byte packet is received by host B, it decodes it
   at 64 kbps, so the extra time needed to decode the first bit in the packet
   is 1 bit / 64000 bits per second = 0.015625 milliseconds. Therefore, the
   total delay between the time the first bit is created and the time it is
   decoded is 17.224 + 0.015625 milliseconds = 17.239625 milliseconds.

4. The end-to-end delay in seconds is

      d = 3 * d_proc
          + L * [(1 / R1) + (1 / R2) + (1 / R3)]
          + (d1 / s1) + (d2 / s2) + (d3 / s3)

   If L = 1500 bytes = 1500 * 8 bits, s1 = s2 = s3 = 2.5 * (10 ^ 8) meters per
   second, R1 = R2 = R3 = 2000000 bits per second, d_proc = 3 milliseconds, d1
   = 5000 kilometers = 5000000 meters, d2 = 4000 kilometers = 4000000 meters,
   and d3 = 1000 kilometers = 1000000 meters, then the end-to-end delay in
   seconds is
   
      d = 3 * 0.003 seconds
          + 12000 * [(1 / 2000000) + (1 / 2000000) + (1 / 2000000)]
          + (5000000 + 4000000 + 1000000 ) / 2.5 * (10 ^ 8)
        = 0.009 + 0.018 + 0.04
        = 0.067 seconds
        = 67 milliseconds

5. Since after NL/R seconds, the entire batch of packets has been transmitted,
   we need only consider the average queuing time of the N packets in a single
   batch. The queuing times are 0, L / R, 2 * L / R, ..., (N - 1) * L / R. The
   arithmetic mean is (1 / N) * (L / R) * (0 + 1 + 2 + ... + (N - 1)), which
   equals L * (N - 1) * (N - 2) / 2 * N * R.

6. Traceroute to intra- and intercontinental hosts at three different times of
   day, starting from host `grubnick.bu.edu`.

   ## Intracontinental host, `github.com` ##

   ### Traced route at 18:07, 20 September 2011 ###

       traceroute to github.com (207.97.227.239), 30 hops max, 60 byte packets
       1  cumm111-0201net-gw.bu.edu (128.197.11.1)  0.987 ms  0.996 ms  1.007 ms
       2  comm595-core-aca01-te3-1-cumm111-dist-aca01-te5-5.bu.edu (128.197.254.165)  1.537 ms  1.557 ms  1.568 ms
       3  comm595-bdr-gw01-gi1-2-comm595-core-aca01-gi2-16.bu.edu (128.197.254.114)  156.464 ms  156.490 ms  156.517 ms
       4  nox300gw1-vl-600-nox-bu.nox.org (207.210.142.237)  0.469 ms  0.537 ms  0.587 ms
       5  nox300gw1-peer-nox-internet2-207-210-142-2.nox.org (207.210.142.2)  20.350 ms  20.404 ms  20.350 ms
       6  64.57.28.75 (64.57.28.75)  43.387 ms  52.519 ms  52.598 ms
       7  * * *
       8  edge3.iad.rackspace.net (207.235.17.129)  12.154 ms  12.136 ms  12.136 ms
       9  vlan905.core5.iad2.rackspace.net (72.4.122.10)  11.918 ms  11.710 ms  11.678 ms
       10  aggr301a-1-core5.iad2.rackspace.net (72.4.122.121)  11.448 ms  11.723 ms  11.566 ms
       11  github.com (207.97.227.239)  11.861 ms  11.861 ms  12.333 ms

   * Average round-trip delay: 12.018 ms
   * Standard deviation: 0.273 ms
   * Number of routers: 10
   * Number of ISPs: 4 (BU, Nox, *, Rackspace)

   ### Traced route at 12:42, 21 September 2011 ###

       traceroute to github.com (207.97.227.239), 30 hops max, 60 byte packets
       1  cumm111-0201net-gw.bu.edu (128.197.11.1)  1.139 ms  1.154 ms  1.168 ms
       2  comm595-core-aca01-te3-1-cumm111-dist-aca01-te5-5.bu.edu (128.197.254.165)  0.846 ms  0.866 ms  0.880 ms
       3  comm595-bdr-gw01-gi1-2-comm595-core-aca01-gi2-16.bu.edu (128.197.254.114)  1.733 ms  1.773 ms  1.800 ms
       4  nox300gw1-vl-600-nox-bu.nox.org (207.210.142.237)  0.427 ms  0.489 ms  0.548 ms
       5  nox300gw1-peer-nox-internet2-207-210-142-2.nox.org (207.210.142.2)  5.119 ms  5.143 ms  5.096 ms
       6  64.57.28.75 (64.57.28.75)  10.502 ms  10.559 ms  10.496 ms
       7  * * *
       8  edge3.iad.rackspace.net (207.235.17.129)  11.874 ms  11.450 ms  11.451 ms
       9  vlan905.core5.iad2.rackspace.net (72.4.122.10)  11.725 ms  11.600 ms  11.802 ms
       10  aggr301a-1-core5.iad2.rackspace.net (72.4.122.121)  11.714 ms  11.621 ms  11.660 ms
       11  github.com (207.97.227.239)  11.525 ms  11.470 ms  11.350 ms

   * Average round-trip delay: 11.448 ms
   * Standard deviation: 0.089 ms
   * Number of routers: 10
   * Number of ISPs: 4 (BU, Nox, *, Rackspace)

   ### Traced route at 21:06, 21 September 2011 ###

       traceroute to github.com (207.97.227.239), 30 hops max, 60 byte packets
       1  cumm111-0201net-gw.bu.edu (128.197.11.1)  1.204 ms  1.212 ms  1.225 ms
       2  comm595-core-aca01-te3-1-cumm111-dist-aca01-te5-5.bu.edu (128.197.254.165)  0.937 ms  0.982 ms  0.981 ms
       3  comm595-bdr-gw01-gi1-2-comm595-core-aca01-gi2-16.bu.edu (128.197.254.114)  0.965 ms  0.974 ms  0.999 ms
       4  nox300gw1-vl-600-nox-bu.nox.org (207.210.142.237)  0.497 ms  0.559 ms  0.618 ms
       5  nox300gw1-peer-nox-internet2-207-210-142-2.nox.org (207.210.142.2)  5.088 ms  5.088 ms  5.079 ms
       6  64.57.28.75 (64.57.28.75)  22.893 ms  22.434 ms  22.391 ms
       7  * * *
       8  edge3.iad.rackspace.net (207.235.17.129)  12.091 ms  12.093 ms  12.072 ms
       9  vlan905.core5.iad2.rackspace.net (72.4.122.10)  12.051 ms  11.529 ms  11.690 ms
       10  aggr301a-1-core5.iad2.rackspace.net (72.4.122.121)  11.683 ms  11.666 ms  11.768 ms
       11  github.com (207.97.227.239)  11.339 ms  11.387 ms  11.379 ms

   * Average round-trip delay: 11.368 ms
   * Standard deviation: 0.026 ms
   * Number of routers: 10
   * Number of ISPs: 4 (BU, Nox, *, Rackspace)

   ## Intercontinental host, `www.cs.ucl.ac.uk` ##

   ### Traced route at 12:50, 21 September 2011 ###

       traceroute to www.cs.ucl.ac.uk (128.16.6.8), 30 hops max, 60 byte packets
       1  cumm111-0201net-gw.bu.edu (128.197.11.1)  1.326 ms  1.337 ms  1.354 ms
       2  comm595-core-aca01-te3-1-cumm111-dist-aca01-te5-5.bu.edu (128.197.254.165)  1.077 ms  1.102 ms  1.115 ms
       3  comm595-bdr-gw01-gi1-2-comm595-core-aca01-gi2-16.bu.edu (128.197.254.114)  2.602 ms  2.634 ms  2.659 ms
       4  nox300gw1-vl-511-nox-bu.nox.org (192.5.89.45)  0.644 ms  0.800 ms  0.869 ms
       5  nox300gw1-peer-nox-internet2-192-5-89-222.nox.org (192.5.89.222)  21.876 ms  22.132 ms  22.157 ms
       6  198.32.11.51 (198.32.11.51)  92.435 ms  92.512 ms  92.448 ms
       7  as1.rt1.lon.uk.geant2.net (62.40.112.138)  100.674 ms  100.563 ms  100.553 ms
       8  janet-gw.rt1.lon.uk.geant2.net (62.40.124.198)  100.585 ms  100.592 ms  100.555 ms
       9  ae12.lond-sbr1.ja.net (146.97.33.137)  100.909 ms  101.269 ms  101.083 ms
       10  be1.londsh-rbr1.ja.net (146.97.35.146)  101.300 ms  101.300 ms  101.465 ms
       11  146.97.137.118 (146.97.137.118)  101.207 ms  101.265 ms  101.334 ms
       12  128.40.125.13 (128.40.125.13)  102.585 ms  102.692 ms  102.646 ms
       13  128.40.20.158 (128.40.20.158)  90.371 ms  90.588 ms  90.431 ms
       14  cisco-cs.ucl.ac.uk (128.40.255.30)  102.826 ms  102.727 ms  102.610 ms
       15  haig.cs.ucl.ac.uk (128.16.6.8)  102.849 ms  102.733 ms  102.819 ms

   * Average round-trip delay: 102.800 ms
   * Standard deviation: 0.060 ms
   * Number of routers: 14
   * Number of ISPs: 5 (BU, Nox, geant2.net, ja.net, UCL)

   ### Traced route at 16:32, 21 September 2011 ###

       traceroute to www.cs.ucl.ac.uk (128.16.6.8), 30 hops max, 60 byte packets
       1  cumm111-0201net-gw.bu.edu (128.197.11.1)  0.978 ms  1.389 ms  1.413 ms
       2  comm595-core-aca01-te3-1-cumm111-dist-aca01-te5-5.bu.edu (128.197.254.165)  1.470 ms  1.491 ms  1.505 ms
       3  comm595-bdr-gw01-gi1-2-comm595-core-aca01-gi2-16.bu.edu (128.197.254.114)  1.305 ms  1.332 ms  1.356 ms
       4  nox300gw1-vl-511-nox-bu.nox.org (192.5.89.45)  0.514 ms  0.580 ms  0.642 ms
       5  nox300gw1-peer-nox-internet2-192-5-89-222.nox.org (192.5.89.222)  5.327 ms  5.378 ms  5.311 ms
       6  198.32.11.51 (198.32.11.51)  92.368 ms  92.368 ms  92.373 ms
       7  as1.rt1.lon.uk.geant2.net (62.40.112.138)  100.493 ms  100.533 ms  100.482 ms
       8  janet-gw.rt1.lon.uk.geant2.net (62.40.124.198)  100.994 ms  101.101 ms  101.094 ms
       9  ae12.lond-sbr1.ja.net (146.97.33.137)  101.457 ms  101.430 ms  101.420 ms
       10  be1.londsh-rbr1.ja.net (146.97.35.146)  101.798 ms  102.146 ms  102.176 ms
       11  146.97.137.118 (146.97.137.118)  101.764 ms  104.480 ms  101.625 ms
       12  128.40.125.13 (128.40.125.13)  103.075 ms  102.818 ms  102.812 ms
       13  128.40.20.158 (128.40.20.158)  90.676 ms  90.914 ms  91.020 ms
       14  cisco-cs.ucl.ac.uk (128.40.255.30)  103.172 ms  103.238 ms  103.226 ms
       15  haig.cs.ucl.ac.uk (128.16.6.8)  104.349 ms  104.569 ms  104.075 ms
 
   * Average round-trip delay: 104.331 ms
   * Standard deviation: 0.24749 ms
   * Number of routers: 14
   * Number of ISPs: 5 (BU, Nox, geant2.net, ja.net, UCL)

   ### Traced route at 21:09, 21 September 2011 ###

       traceroute to www.cs.ucl.ac.uk (128.16.6.8), 30 hops max, 60 byte packets
       1  cumm111-0201net-gw.bu.edu (128.197.11.1)  1.147 ms  1.159 ms  1.173 ms
       2  comm595-core-aca01-te3-1-cumm111-dist-aca01-te5-5.bu.edu (128.197.254.165)  1.003 ms  0.999 ms  1.009 ms
       3  comm595-bdr-gw01-gi1-2-comm595-core-aca01-gi2-16.bu.edu (128.197.254.114)  0.974 ms  0.985 ms  1.006 ms
       4  nox300gw1-vl-511-nox-bu.nox.org (192.5.89.45)  0.432 ms  0.485 ms  0.544 ms
       5  nox300gw1-peer-nox-internet2-192-5-89-222.nox.org (192.5.89.222)  5.059 ms  5.059 ms  5.050 ms
       6  198.32.11.51 (198.32.11.51)  92.594 ms  92.508 ms  92.462 ms
       7  as1.rt1.lon.uk.geant2.net (62.40.112.138)  100.497 ms  100.490 ms  100.473 ms
       8  janet-gw.rt1.lon.uk.geant2.net (62.40.124.198)  100.726 ms  100.690 ms  100.674 ms
       9  ae12.lond-sbr1.ja.net (146.97.33.137)  100.900 ms  101.083 ms  101.074 ms
       10  be1.londsh-rbr1.ja.net (146.97.35.146)  101.480 ms  101.627 ms  101.498 ms
       11  146.97.137.118 (146.97.137.118)  101.488 ms  101.288 ms  101.519 ms
       12  128.40.125.13 (128.40.125.13)  102.494 ms  102.928 ms  103.031 ms
       13  128.40.20.158 (128.40.20.158)  90.997 ms  90.731 ms  90.551 ms
       14  cisco-cs.ucl.ac.uk (128.40.255.30)  102.987 ms  102.486 ms  102.469 ms
       15  haig.cs.ucl.ac.uk (128.16.6.8)  103.188 ms  102.540 ms  103.047 ms
 
   * Average round-trip delay: 102.925 ms
   * Standard deviation: 0.341 ms
   * Number of routers: 14
   * Number of ISPs: 5 (BU, Nox, geant2.net, ja.net, UCL)

7. 
   1. The bandwidth-delay product is

        R * d_prop = (2 * (10 ^ 6) bits per second)
                     * 2 * 10 ^ 7 meters / 2.5 * 10 ^ 8 meters per second
                   = (4 * (10 ^ 13) / (2.5 * (10 ^ 8))) bits
                   = 1.6 * 10 ^ 5 bits

   2. If we can only send one bit at a time sequentially on the link, then the
      total number of bits that can be in the link at any given time will be
      the bandwidth-delay product, 1.6 * 10 ^ 5 bits = 160000 bits.

   3. The bandwidth-delay product is the maximum number of bits which can be on
      the link at any given time.

   4. The width of a bit on this link is 2 * 10 ^ 7 meters per link / 1.6 * 10
      ^ 5 bits per link = 200 meters / 1.6 bits = 125 meters per bit. This is
      longer than a football field.

   5. The width of a bit in meters is m / (R * (m / s)) = s / R.

8. 
   1. The delay required to move the message from the source host to the first
      packet switch is the transmission delay, which is 8 * 10 ^ 6 bits / 2 *
      10 ^ 6 bits per second = 4 seconds. The delay to reach the second packet
      switch from the first is the same, and the delay to reach the destination
      host from the second packet switch is the same as well. Therefore, the
      total end-to-end delay is 3 * 4 seconds = 12 seconds.

   2. Suppose the message is segmented into 4000 packets of 2000 bits each. To
      move the first packet from the source host to the first packet switch is
      2 * 10 ^ 3 bits / 2 * 10 ^ 6 bits per second = .001 seconds, or 1
      millisecond. After 2 * 1 millisecond, the second packet will be fully
      received at the first packet switch.

   3. The total time to complete sending all the packets is the total time is
      (4000 + 2) * 1 millisecond = 4.002 seconds. This is less than the time of
      sending the entire message as one large packet because we are better
      utilizing the "pipeline". While waiting for one small packet to reach its
      destination, we can concurrently send another packet, and another, etc.

   4. The drawbacks of this system include (1) the processing time required for
      segmentation and reassembly, (2) a greater chance of packets being
      dropped, since there are more packets, and (3) the space overhead
      necessary for each packet.

9. The ultimately transmitted message has length M + h * n bytes, so the
   fraction which is comprised of header information is h * n / (M + h * n).

10. The table below shows the total overhead plus data loss in bytes as it
    depends on packet (data) size in bytes.

      +=============+===========+================+===========+================+
      | packet size | number of | total overhead | data loss | total overhead |
      |    (bytes)  |  packets  |     (bytes)    |  (bytes)  |  + lost data   |
      +=============+===========+================+===========+================+
      |     1000    |    1000   |     100000     |    1000   |     101000     |
      |     5000    |     200   |      20000     |    5000   |      25000     |
      |    10000    |     100   |      10000     |   10000   |      20000     |
      |    20000    |      50   |       5000     |   20000   |      25000     |
      +-------------+-----------+----------------+-----------+----------------+

    For a message of one million bytes, a packet size of 10000 bytes is optimal
    because it has minimum total overhead plus data lost, assuming one packet
    is lost.
