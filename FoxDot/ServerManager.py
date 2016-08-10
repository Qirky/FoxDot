"""
    ServerManager.py

    Handles OSC messages being sent to SuperCollider. Will try and
    read data from Settings/server.txt which should contain the IP
    address and port separated by a single space. If not it defaults
    to SuperCollider's defaults.

"""

from OSC import *
from subprocess import Popen
from time import sleep
from Settings import *
import os

class ServerManager:

    def __init__(self, addr=ADDRESS, port=int(PORT)):

        self.addr = addr
        self.port = port
        
        self.client = OSCClient()
        self.client.connect( (self.addr, self.port) )

        self.sclang = OSCClient()
        self.sclang.connect( (self.addr, self.port + 10) ) # TODO

        self.node = 1000

        self.booted=False

        debug = 0
        msg = OSCMessage("/dumpOSC")
        msg.append(debug)
        self.client.send(msg)

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

    # Boot and Quit
    # -------------

    def boot(self):
        if not self.booted:
            conf = os.path.realpath(FOXDOT_ROOT + OSC_FUNC)
            print conf
            exe  = "sclang.exe"
            os.chdir(SC_DIRECTORY)
            print "Booting SuperCollider Server...",
            self.daemon = Popen([exe, '-D', conf])
            sleep(5)
            # TODO
            # While no reply:
            #   sleep(1)
            os.chdir(USER_CWD)
            self.booted=True
        else:
            print "Warning: SuperCollider already booted"
        return

    def quit(self):
        if self.booted:
            print "Quitting SuperCollider Server"
            self.client.send(OSCMessage("/quit"))
            sleep(0.5)
            self.daemon.terminate()
        return
    

Server = ServerManager()
