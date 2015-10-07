# CS655 lab 1 #

Jeffrey Finkelstein
29 September 2011

1. protocols: IGMP, DNS, TCP, HTTP, ARP
2. time between HTTP GET and HTTP OK: 46.567866 - 46.549688 = 0.018178
3. gaia.cs.umass.edu is at 128.119.245.12, mine is 192.168.1.140
4. printed packets below:

      No.     Time        Source                Destination           Protocol Info
          234 46.549688   192.168.1.140         128.119.245.12        HTTP     GET /wireshark-labs/INTRO-wireshark-file1.html HTTP/1.1 

      Frame 234: 513 bytes on wire (4104 bits), 513 bytes captured (4104 bits)
      Ethernet II, Src: IntelCor_44:8c:2f (00:13:ce:44:8c:2f), Dst: Cisco-Li_f7:57:de (00:1a:70:f7:57:de)
      Internet Protocol, Src: 192.168.1.140 (192.168.1.140), Dst: 128.119.245.12 (128.119.245.12)
      Transmission Control Protocol, Src Port: 43494 (43494), Dst Port: http (80), Seq: 1, Ack: 1, Len: 447
      Hypertext Transfer Protocol
          GET /wireshark-labs/INTRO-wireshark-file1.html HTTP/1.1\r\n
          Host: gaia.cs.umass.edu\r\n
          Connection: keep-alive\r\n
          User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/13.0.782.218 Chrome/13.0.782.218 Safari/535.1\r\n
          Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
          Accept-Encoding: gzip,deflate,sdch\r\n
          Accept-Language: en-US,en;q=0.8\r\n
          Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\r\n
          \r\n

      No.     Time        Source                Destination           Protocol Info
          236 46.567866   128.119.245.12        192.168.1.140         HTTP     HTTP/1.1 200 OK  (text/html)

      Frame 236: 446 bytes on wire (3568 bits), 446 bytes captured (3568 bits)
      Ethernet II, Src: Cisco-Li_f7:57:de (00:1a:70:f7:57:de), Dst: IntelCor_44:8c:2f (00:13:ce:44:8c:2f)
      Internet Protocol, Src: 128.119.245.12 (128.119.245.12), Dst: 192.168.1.140 (192.168.1.140)
      Transmission Control Protocol, Src Port: http (80), Dst Port: 43494 (43494), Seq: 1, Ack: 448, Len: 380
      Hypertext Transfer Protocol
          HTTP/1.1 200 OK\r\n
          Date: Thu, 29 Sep 2011 02:29:37 GMT\r\n
          Server: Apache/2.2.3 (CentOS)\r\n
          Last-Modified: Thu, 29 Sep 2011 02:29:02 GMT\r\n
          ETag: "8734b-51-45935780"\r\n
          Accept-Ranges: bytes\r\n
          Content-Length: 81\r\n
          Keep-Alive: timeout=10, max=100\r\n
          Connection: Keep-Alive\r\n
          Content-Type: text/html; charset=UTF-8\r\n
          \r\n
      Line-based text data: text/html
