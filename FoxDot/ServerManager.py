"""
    ServerManager.py

    Handles OSC messages being sent to SuperCollider.

"""

from OSC import *
from Settings import *

import socket
from subprocess import Popen
from time import sleep
import os

class ServerManager:

    def __init__(self, addr=ADDRESS, port=int(PORT)):

        self.addr = addr
        self.port = port
        self.SCLang_port = port + 10 # TODO

        self.booted = False
        self.wait_time = 5
        self.count = 0

        self.boot()
        
        self.client = OSCClient()
        self.client.connect( (self.addr, self.port) )

        self.sclang = OSCClient()
        self.sclang.connect( (self.addr, self.SCLang_port) )

        self.node = 1000

        # Toggle debug
        # ------------

        self.dumpOSC(0)

    def __str__(self):
        return "FoxDot ServerManager Instance -> {}:{}".format(self.addr, self.port)

    def __repr__(self):
        return str(self)

    def nextnodeID(self):
        self.node += 1
        return self.node

    def sendOSC(self, packet):
        """ Compiles and sends an OSC message for SuperCollider """
        message = OSCMessage("/s_new")
        packet[1] = self.nextnodeID()
        message.append(packet)
        self.client.send( message )
        return

    def sendNote(self, SynthDef, packet):
        packet = [SynthDef, 0, 1, 1] + packet
        self.sendOSC(packet)
        return

    def send(self, message):
        self.client.send(OSCMessage(message))
        return

    def free_node(self, node):
        message = OSCMessage("/n_free")
        message.append(node)
        self.client.send( message )
        return

    # Buffer Communiation
    # -------------------

    def bufferRead(self, bufnum, path):
        message = OSCMessage("/b_allocRead")
        message.append([bufnum, path])
        self.client.send( message )
        return

    # SynthDef Commmunication
    # -----------------------

    def loadSynthDef(self, fn, cmd='/foxdot'):
        msg = OSCMessage()
        msg.setAddress(cmd)
        msg.append(fn)
        self.sclang.send(msg)
        return

    # Debug - Dumps OSC messages SCLang side
    # --------------------------------------

    def dumpOSC(self, value=1):
        msg = OSCMessage("/dumpOSC")
        msg.append(value)
        self.client.send(msg)
        return


    # Boot and Quit
    # -------------

    def boot(self):

        print self.count
        self.count += 1

        if not self.booted:
            
            conf = os.path.realpath(FOXDOT_ROOT + OSC_FUNC)
            
            os.chdir(SC_DIRECTORY)
            
            print "Booting SuperCollider Server..."
            
            self.daemon = Popen([SCLANG_EXEC, '-D', conf])

            sleep(self.wait_time)

            os.chdir(USER_CWD)

            self.booted = True

        else:
            
            print "Warning: SuperCollider already running"
            
        return

    def quit(self):
        if self.booted:
            self.client.send(OSCMessage("/quit"))
            sleep(0.5)
            self.daemon.terminate()
        return

if __name__ != "__main__":

    # don't boot server unless imported

    Server = ServerManager()
