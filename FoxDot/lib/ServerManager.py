"""
    ServerManager.py

    Handles OSC messages being sent to SuperCollider.

"""

import os, socket
from subprocess import Popen
from time import sleep

from Settings import *
from OSC import *

class SCLangClient(OSCClient):
    def send(*args, **kwargs):
        try:
            OSCClient.send(*args, **kwargs)
        except Exception as e:
            print(e)

class SCLangServerManager:

    def __init__(self, addr, osc_port, sclang_port):

        self.addr = addr
        self.port = osc_port
        self.SCLang_port = sclang_port

        self.booted = False
        self.wait_time = 5
        self.count = 0
        
        self.client = SCLangClient()
        self.client.connect( (self.addr, self.port) )

        self.sclang = SCLangClient()
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
        node = packet[1] = self.nextnodeID()
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
        """ Don't use """

        if not self.booted:
            
            os.chdir(SC_DIRECTORY)
            
            print("Booting SuperCollider Server...")
            
            self.daemon = Popen([SCLANG_EXEC, '-D', FOXDOT_STARTUP_FILE])

            os.chdir(USER_CWD)

            self.booted = True

        else:
            
            print("Warning: SuperCollider already running")
            
        return

    def start(self):
        ''' Boot SuperCollider and connect over OSC '''

        # 1. Compile startup file

        with open(FOXDOT_STARTUP_FILE, 'w') as startup:

            startup.write('''Routine.run {
                	s.options.blockSize = 128;
                        s.options.memSize = 131072;
                        s.bootSync();\n''')

            files = [FOXDOT_OSC_FUNC, FOXDOT_BUFFERS_FILE] + GET_SYNTHDEF_FILES()

            for fn in files:

                f = open(fn)
                startup.write(f.read())
                startup.write("\n")

            startup.write("};")

        # 2. Boot SuperCollider

        self.boot()

        return

    def quit(self):
        if self.booted:
            self.client.send(OSCMessage("/quit"))
            sleep(0.5)
            self.daemon.terminate()
        return


if __name__ != "__main__":

    from Settings import ADDRESS, PORT, PORT2

    Server = SCLangServerManager(ADDRESS, PORT, PORT2)
