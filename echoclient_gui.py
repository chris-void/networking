#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: Zhiqiang Ren
last modified: Sep. 2013
"""

import Tkinter as tk

from Tkinter import Frame, Button, Entry, Text, Label, Message

import echoclient as ec
import struct

class Client(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, relief=tk.RAISED, borderwidth=10)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        self.parent.title("Client")
        frame = Frame(self, relief=tk.RAISED, borderwidth=1)

        # The width of the first column gets almost no change.
        frame.columnconfigure(0, pad=10, weight=1)
        frame.columnconfigure(1, pad=10, weight=1000)

        lbl_addr = Label(frame, text="Address")
        lbl_addr.grid(row=0,column=0, sticky=tk.W+tk.S)

        lbl_port = Label(frame, text="Port")
        lbl_port.grid(row=0,column=1, sticky=tk.W+tk.S)

        ent_addr = Entry(frame, width=15)
        ent_addr.grid(row=1,column=0, sticky=tk.W+tk.N)

        ent_port = Entry(frame, width=6)
        ent_port.grid(row=1,column=1, sticky=tk.W+tk.N)

        lbl_msg = Label(frame, text="Input Message", anchor=tk.E)
        lbl_msg.grid(row=2,column=0, sticky=tk.W+tk.S)

        ent_msg = Text(frame, width=30, height=4)
        ent_msg.grid(row=3,column=0, columnspan=2, sticky=tk.W+tk.E+tk.N) # sticky can be used to expand

        lbl_num = Label(frame, text="Input Number")
        lbl_num.grid(row=4,column=0, sticky=tk.W+tk.S)

        ent_num = Entry(frame, width=6)
        ent_num.grid(row=5,column=0, sticky=tk.W+tk.N)
        # ======================

        ret_indicator = tk.StringVar()
        ret_indicator.set("Result")
        lab_res = Label(frame, textvariable=ret_indicator)
        lab_res.grid(row=6,column=0, sticky=tk.W+tk.S)

        var_res = tk.StringVar()
        msg_res = Message(frame,textvariable=var_res, width=500)
        msg_res.grid(row=7,column=0, columnspan=2,sticky=tk.W+tk.E+tk.N)

        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        def connect():
            self.addr = ent_addr.get()
            portStr = ent_port.get()

            if self.addr == "":
                self.addr = "localhost"

            if portStr == "":
                self.port = 50000
            else:
                self.port = int(portStr)

            (ret, info) = ec.connect(self.addr, self.port)
            if ret == 0:
                ret_indicator.set("Connection Succeeded")
                self.conn = info
                var_res.set("")
            else:
                ret_indicator.set("Connection Failed")
                var_res.set(info)

        def sendMsg():
            msg = ent_msg.get("0.0", tk.END)[0:-1]
            print "msg to be sent is: " + repr(msg)
            (ret, info) = ec.sendMsg(self.conn, msg.encode('utf-8'))
            if ret == 0:
                ret_indicator.set("Send Succeeded")
                var_res.set("")
            else:
                ret_indicator.set("Send Failed")
                var_res.set(info)

        def sendNum():
            msg = ent_num.get()
            print "msg to be sent is: " + repr(msg)
            (ret, info) = ec.sendNum(self.conn, int(msg))
            if ret == 0:
                ret_indicator.set("Send Succeeded")
                var_res.set("")
            else:
                ret_indicator.set("Send Failed")
                var_res.set(info)

        def recvMsg():
            (ret, info) = ec.recvMsg(self.conn)
            if ret == 0:
                ret_indicator.set("Receive Succeeded")
            else:
                ret_indicator.set("Receive Failed")
            var_res.set(info)

        def close():
            (ret, info) = ec.close(self.conn)
            if ret == 0:
                ret_indicator.set("Close Succeeded")
                var_res.set("")
            else:
                ret_indicator.set("Close Failed")
                var_res.set(info)

        frame2 = Frame(self, relief=tk.RAISED, borderwidth=1)

        """Buttoms are always in the middle."""
        frame2.columnconfigure(0, pad=10, weight=1)
        frame2.rowconfigure(0, weight=1000)
        frame2.rowconfigure(1, weight=1)
        frame2.rowconfigure(2, weight=1)
        frame2.rowconfigure(3, weight=1)
        frame2.rowconfigure(4, weight=1)
        frame2.rowconfigure(5, weight=1)
        frame2.rowconfigure(6, weight=1000)

        but_conn = Button(frame2, text="Connect", command=connect)
        but_conn.grid(row=1,column=0, sticky=tk.W+tk.E)

        but_send_msg = Button(frame2, text="Send Message", command=sendMsg)
        but_send_msg.grid(row=2,column=0, sticky=tk.W+tk.E)

        but_send_num = Button(frame2, text="Send Number", command=sendNum)
        but_send_num.grid(row=3,column=0, sticky=tk.W+tk.E)

        but_recv = Button(frame2, text="Receive", command=recvMsg)
        but_recv.grid(row=4,column=0, sticky=tk.W+tk.E)

        but_close = Button(frame2, text="Close", command=close)
        but_close.grid(row=5,column=0, sticky=tk.W+tk.E)

        frame2.pack(side=tk.LEFT, fill=tk.BOTH,expand=1)

        # expand=1 cannot be omitted
        self.pack(fill=tk.BOTH, expand=1)

def main():
  
    root = tk.Tk()
    # root.geometry("300x200+300+300")
    root.geometry("+500+500")
    app = Client(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

