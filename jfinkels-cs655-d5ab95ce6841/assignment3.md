# CS655 assignment 3 #

Jeffrey Finkelstein
1 December 2011

All problems are from chapter 4 in Kurose and Ross.

9. The forwarding table looks like

      destination       | link
      ==================+=====
      11100000 00       |   0
      11100000 01000000 |   1
      1110000           |   2
      11100001 1        |   3
      otherwise         |   3

  The datagram

      11001000 10010001 01010001 01010101

  has no longest prefix match with any of the four explicit destination
  addresses, so it is forward to link 3 (the "otherwise" case).

  The datagram

      11100001 01000000 11000011 00111100

  has longest prefix match with `1110000`, so it is forwarded to link 2.

  The datagram

      11100001 10000000 00010001 01110111

  has longest prefix match with `11100001 1`, so it is forwarded to link 3.

12. One possible choice of three network address ranges is

        11011111 00000001 00010001 00000000
          through
        11011111 00000001 00010001 00111111

        11011111 00000001 00010001 01000000
          through
        11011111 00000001 00010001 10011111

        11011111 00000001 00010001 10100000
          through
        11011111 00000001 00010001 10101111

  so the routing table would look like this

                          destination  | link
       ================================+=====
       11011111 00000001 00010001 00   |  1
       11011111 00000001 00010001      |  2
       11011111 00000001 00010001 1010 |  3

  so the three address ranges, assuming longest-prefix matching, should be

       223.1.17.  0 / 26
       223.1.17. 64 / 24
       223.1.17.160 / 28

17. Assume the original datagram has 20 bytes of IP header and 2380 bytes of
  payload data. Datagrams on a network with a MTU of 700 bytes will have 20
  bytes of IP header plus 680 bytes of payload. The datagram is fragmented into
  ceiling(2380 / 680) = 4 fragments. The fields related to fragmentation in the
  generated IP datagrams are described by the following table.
  
         fragment | bytes |  ID | offset | flag
        ==========+=======+=====+========+======
            1     |  680  | 422 |     0  |   1
            2     |  680  | 422 |    85  |   1
            3     |  680  | 422 |   170  |   1
            4     |  340  | 422 |   255  |   0

24. Shortest paths from node x to all other nodes can be computed using
  Dijkstra's algorithm as follows. ∞

         |         |        pairs of the form
         |         |     (distance, predecessor)
         |         |         to other nodes
    step |    N'   |  t  |  u  |  v  |  w  |  y  |  z 
   ======+=========+=====+=====+=====+=====+=====+=====
     0   | x       |  ∞  |  ∞  | 3,x | 6,x | 6,x | 8,x
     1   | vx      | 7,v | 6,v |     | 6,x | 6,x | 8,x
     2   | uvx     | 7,v |     |     | 6,x | 6,x | 8,x
     3   | tuvx    |     |     |     | 6,x | 6,x | 8,x
     4   | tuvwx   |     |     |     |     | 6,x | 8,x
     5   | tuvwxy  |     |     |     |     |     | 8,x
     6   | tuvwxyz |     |     |     |     |     |

  Shortest paths to each node can be computed using the predecessors from the
  bottom-most non-blank entry in each node column.

28. (a) x's distance vector is {w: 2, y: 4, u: 7}.
  (b) If c(x, w) changes to 1, then x's minimum distance to u will be 6 (via
  w), so it will inform its neighbors.
  (c) If c(x, y) changes to 100, then x's minimum distance to u will remain 7
  (via w), so it will not inform its neighbors of a change.

35. (a) Router 3c learns about prefix x from routing protocol eBGP (from the
  router 4c in AS4).
  (b) Router 3a learns about x from iBGP (from router 3c via 3b in AS3).
  (c) Router 1c learns about x from eBGP (from router 3a in AS3).
  (d) Router 1d learns about x from iBGP (from router 1c via 1a [or 1b] in
  AS3).
