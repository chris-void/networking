//package pa3;
/*Deemah AlEyoni
 CS655
 BUID: 

 import java.io.*;

 /**
 * This is the class that students need to implement. The code skeleton is provided.
 * Students need to implement rtinit(), rtupdate() and linkhandler().
 * printdt() is provided to pretty print a table of the current costs for reaching other nodes in the network.
 */

public class Node {

    public static final int INFINITY = 9999;

    int[] lkcost;		/*The link cost between node 0 and other nodes*/
    int[][] costs;  		/*Define distance table costs*/
    int[][] preFinals;          /*Define distance table prefianls*/
    int nodename;             /*Name of this node*/

    // dest, VIA
    int[][] rt;                // RoutingTable
    int[][] distanceV;           // distance Vector of node to be advertised to neighbours.
    int size = 4;

    /* Class constructor */
    public Node() {
    }

    /* students to write the following two routines, and maybe some others */
    void rtinit(int nodename, int[] initial_lkcost) {
        this.nodename = nodename;
        this.lkcost = initial_lkcost;
        this.costs = new int[size][size];
        this.preFinals = new int [size][size];
        this.distanceV = new int[size][size];
        this.rt = new int[size][3];

        // intaliazation of the distance table, intialize all with 9999 then reassign with the lkcost.
        // intialiaztion of prefinal nodes. 
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                this.costs[i][j] = 9999;
                this.preFinals[i][j]= -1;
            }
        }
        
        // update the costs table.
        this.costs[0][0] = this.lkcost[0];
        this.costs[1][1] = this.lkcost[1];
        this.costs[2][2] = this.lkcost[2];
        this.costs[3][3] = this.lkcost[3];
        
        // Upating theprefinal nodes. 
        this.preFinals[0][0] = this.nodename;
        this.preFinals[1][1] = this.nodename;
        this.preFinals[2][2] = this.nodename;
        this.preFinals[3][3] = this.nodename;
        
        
        //Creating  advertised table of cost to be sent to neighbors -- distanceV
        //distanceV first column will hold costs. second column will hold VIA nodes.
        //rt will now hold cost, via, prefinal
        for (int i = 0; i < size; i++) {
            this.distanceV[i][0] = this.lkcost[i]; //assign cost to advertised table.
            this.distanceV[i][1] = this.preFinals[i][i]; //assign prefinal node. 
            rt[i][0] = this.lkcost[i]; // assign cost to routing table.
            if (this.lkcost[i] == INFINITY) {
                rt[i][1] = -1;
                rt[i][2] =-1; 
            } else {
                this.rt[i][1] = i; // assign via node.
                this.rt[i][2] =this.nodename; //assign the pre final node. 
            }

        }

        //send to neighburs only
        for (int i = 0; i < size; i++) {
            if (this.lkcost[i] != 9999 && i != this.nodename) //Dont to send to non neighbours(infinity distance)& Dont send to itself.
            {
                //Packet(int sourceid, int destid, int[] distanceV)
                Packet p1 = new Packet(this.nodename, i, this.distanceV);
                NetworkSimulator.tolayer2(p1);
            }
        }

        printdt();
        printRoutingTable();

    }

    
    void printRoutingTable() {

    
        System.out.println("Routing table of Node: " + this.nodename);
        System.out.println("Destination\tCost\t\tNextHop\t\tPreFinal Node");
        for (int i = 0; i < this.lkcost.length; i++) {
            System.out.println(i + "\t\t" + this.rt[i][0] + "\t\t" + this.rt[i][1]+"\t\t" + this.rt[i][2]);

        }
       
        System.out.println("");
    }

    void rtupdate(Packet rcvdpkt) {
        int destination = rcvdpkt.destid;
        int source = rcvdpkt.sourceid;

        System.out.println(destination + " has recived an update from " + source);

        // now we should update the distance table according to the newly recived information.
        // we will check only the <<via>> that coresponds to the source. 
        boolean costTablechanged = false;

        for (int i=0; i<size; i++){
            
        }
        
        // update rt, cost, 
        
        
        


        for (int i = 0; i < size; i++) {
            if (this.costs[i][source] != rcvdpkt.mincost[i]) {
                costTablechanged = true;
                if (rcvdpkt.mincost[i] == INFINITY) {// firt check if the new update is INFINITY to assign it directly 
                    this.costs[i][source] = INFINITY;

                } else { // if it is not then update the with the new cost + the cost of link between the two nodes. 

                    this.costs[i][source] = rcvdpkt.mincost[i] + this.lkcost[source];
                }
            }
        }

        if (costTablechanged) {
            System.out.println("*****Cost Table has changed*****");

        } else {
            System.out.println("*****Cost table didnt change*****");
        }
        
        updateRouting();
        
    }

    /* called when cost from the node to linkid changes from current value to newcost*/
    void linkhandler(int linkid, int newcost) {
        System.out.println("#########################################################");
        System.out.println("The link cost has changed between this node "
                + this.nodename + " and neighbour node " + linkid+ " to " + newcost);
        System.out.println("#########################################################");
        // first we calculate the difference between the new and old

        for (int i=0; i<size; i++){
            this.costs[i][linkid] = 
        }
        
        
        
        
        
        int diff = newcost - this.lkcost[linkid];
        this.lkcost[linkid] = newcost;
        
        //now update the distance table for the specific link
        System.out.println("*****Updating Distance table because of Link cost change*****");
        for ( int i =0; i<size ;i++)
        {
            if (this.costs[i][linkid] != INFINITY)
            {
            this.costs[i][linkid]= (this.costs[i][linkid] + diff);
            }
        }
       
        // check if the routing table has changed or not, send updates if it did. 
        // this is the same as rtupdate for checking for min cost after updating the distance table
        
        //update this.distanceV and routing table. if changed asdvertise to neighbours. 
        updateRouting();
    }

    /*
     * return the path from cur node to node j
     */
     void pathTo(int j){
        int[] path;
        int pivot = j;
        path.append(pivot);
        
        while (pivot != nodename){
            path.append(pivot);
            pivot = rt[pivot][2];
        }
        
        // reverse path and print 
        for (int i=path.length; i!= 0; i--)
            print path[i];
        
     }

    void inPath()
    
    void updateRouting()
    {



        
        int[] oldDistanceV = new int[this.distanceV.length];
        // first make copy of the original distanceV.
        for (int i = 0; i < oldDistanceV.length; i++) {
            oldDistanceV[i] = this.distanceV[i];
        }

        // loop through the updated cost table to find the new minCost(distanceV)
        for (int destenation = 0; destenation < size; destenation++) {
            //find minimum for each detenation. 
            int min = this.costs[destenation][0];
            int nextHop = 0;
            for (int via = 1; via < this.distanceV.length; via++) {
                if (this.costs[destenation][via] < min) {
                    min = this.costs[destenation][via];
                    nextHop = via;
                }
            }
            this.distanceV[destenation] = min;
            this.rt[destenation][0] = min;
            this.rt[destenation][1] = nextHop;
        }

        //compare the old/new distanceV(minCost) to decide if it has changed to advertise the new update. 
        boolean updated = false;
        for (int i = 0; i < distanceV.length; i++) {
            if (oldDistanceV[i] != this.distanceV[i]) {
                updated = true;
            }
        }

        if (updated) {
            System.out.println("*****Routing Table has changed*****");
            System.out.println("*****Sending Updates to neighbours*****");
            //Packet(int sourceid, int destid, int[] distanceV

            //update neighbours using poisn reverse 
            for (int i = 0; i < size; i++) {
                int[] poisoncost = new int[size];
                for (int newI = 0; newI < size; newI++) {
                    poisoncost[newI] = this.distanceV[newI];
                }
                if (this.lkcost[i] != 9999 && i != this.nodename) //Dont to send to non neighbours(infinity distance)& Dont send to itself.
                {
                    for (int index = 0; index < size; index++) {
                        // here we are checing the RoutingTable for Nexthop. any neighbour that we are using in our Routing table, will be poisoned
                        // meaning, we will update the cost for that destenation to INFINITY. 
                        if (this.rt[index][1] == i) {
                            poisoncost[index] = INFINITY;
                        }
                    }
                    System.out.println("The distane vector being sent to node: " + i + " from " + this.nodename);
                    for (int x = 0; x < size; x++) {
                        System.out.println("Destenation: " + x + " cost: " + poisoncost[x]);
                    }
                    //Packet(int sourceid, int destid, int[] distanceV)
                    Packet p1 = new Packet(this.nodename, i, poisoncost);
                    NetworkSimulator.tolayer2(p1);
                }

            }

        } else {
            System.out.println("*****Routing table didnt change*****");

        }

        printdt();
        printRoutingTable();

    }


    
    /* Prints the current costs to reaching other nodes in the network */
    void printdt() {
        switch (nodename) {
            case 0:
                System.out.printf("                via     \n");
                System.out.printf("   D0 |    1     2    3 \n");
                System.out.printf("  ----|-----------------\n");
                System.out.printf("     1|  %3d   %3d   %3d\n", costs[1][1], costs[1][2], costs[1][3]);
                System.out.printf("dest 2|  %3d   %3d   %3d\n", costs[2][1], costs[2][2], costs[2][3]);
                System.out.printf("     3|  %3d   %3d   %3d\n", costs[3][1], costs[3][2], costs[3][3]);
                break;
            case 1:
                System.out.printf("                via     \n");
                System.out.printf("   D1 |    0     2 \n");
                System.out.printf("  ----|-----------------\n");
                System.out.printf("     0|  %3d   %3d \n", costs[0][0], costs[0][2]);
                System.out.printf("dest 2|  %3d   %3d \n", costs[2][0], costs[2][2]);
                System.out.printf("     3|  %3d   %3d \n", costs[3][0], costs[3][2]);
                break;

            case 2:
                System.out.printf("                via     \n");
                System.out.printf("   D2 |    0     1    3 \n");
                System.out.printf("  ----|-----------------\n");
                System.out.printf("     0|  %3d   %3d   %3d\n", costs[0][0], costs[0][1], costs[0][3]);
                System.out.printf("dest 1|  %3d   %3d   %3d\n", costs[1][0], costs[1][1], costs[1][3]);
                System.out.printf("     3|  %3d   %3d   %3d\n", costs[3][0], costs[3][1], costs[3][3]);
                break;
            case 3:
                System.out.printf("                via     \n");
                System.out.printf("   D3 |    0     2 \n");
                System.out.printf("  ----|-----------------\n");
                System.out.printf("     0|  %3d   %3d\n", costs[0][0], costs[0][2]);
                System.out.printf("dest 1|  %3d   %3d\n", costs[1][0], costs[1][2]);
                System.out.printf("     2|  %3d   %3d\n", costs[2][0], costs[2][2]);
                break;
        }
    }
}
// this is taking too long to solve :( :( :(
// wala ya wala ya wala ya a yaaaaaa PA3
