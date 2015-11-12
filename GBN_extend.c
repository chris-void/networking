#define     FALSE           0
#define     TRUE            1

extern int nsimmax;             // maximum number of messages sent
extern double lossProb;         // loss probability
extern double corruptProb;      // corruption probability

// Entity A
int txBase;                     // first sequence number of window
int nextSeqNum;                 // last sequence number within window
int nextMsg;                    // message index
msg *msgBuffer;                 // message buffer
pkt *txPktBuffer;               // packet buffer
int msgCount;                   // message count

// Entity B
int expectSeqNum;               // expected sequence number
int lastAckNum;                 // last acknowledgement number

// Statistics
int txPktCount;                 // count of packets sent by A
int rxPktCount;                 // count of packets received by B
int corruptPktCount;            // count of corrupted packets received by B
int rxmtCount;                  // retransmit count
double *txPktTime;              // transmit time of each packet
double totalTtc;                // total time to communicate
int commPktCount;               // count of communicated packets
int receivedMsgCount;           // count of messages received by B
double *msgArriveTime;          // arrival times of each message
double totalDelay;              // total queuing delay

// Print window
void printWindow(int base)
{
    int i, end = (base + WINDOW_SIZE) % LIMIT_SEQNUM;

    printf("    WINDOW: [");
    for (i = base; i != end; i = (i + 1) % LIMIT_SEQNUM)
        printf(" %d", i);
    printf(" ]\n");
}

// Check if number is within window
int isWithinWindow(int base, int i)
{
    // Number located right of base
    int right = i >= base && i < base + WINDOW_SIZE;

    // Number located left of base
    int left = i < base && i + LIMIT_SEQNUM < base + WINDOW_SIZE;
    
    return right || left;
}

// Calculate checksum of packet
int calcChecksum(pkt packet)
{
    int i, checksum = 0;

    checksum += packet.seqnum;
    checksum += packet.acknum;

    for (i = 0; i < 20; i++)
        checksum += packet.payload[i];

    return checksum;
}

// Check packet for errors
int isCorrupt(pkt packet)
{
    return calcChecksum(packet) - packet.checksum;
}



//////////////


