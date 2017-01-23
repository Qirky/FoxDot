"""
    ServerManager.py

    Handles OSC messages being sent to SuperCollider.

"""

import os, socket
from subprocess import Popen
from time import sleep

from Effects import FxList

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

        self.node = 1100 # The first 100 are reserved
        self.bus  = 4

        self.fx_setup_done = False
        self.fx_nodes = {}

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

    def nextbusID(self):
        if self.bus > 100:
            self.bus = 4
        self.bus += 1
        return self.bus

    def sendOSC(self, packet):
        """ Compiles and sends an OSC message for SuperCollider """
        message = OSCMessage("/s_new")
        node = packet[1] = self.nextnodeID()
        message.append(packet)
        self.client.send( message )        
        return

    def sendNote(self, SynthDef, packet):
        packet = [SynthDef, 0, 1, 1] + packet
        message = OSCMessage("/s_new")
        node = packet[1] = self.nextnodeID()
        message.append(packet)
        self.client.send( message )   
        return

    def fx_setup(self):
        bundle = OSCBundle()
        msg=OSCMessage("/s_new")
        packet = ["makeSound", 1001, 1, 1]
        msg.append(packet)
        bundle.append(msg)

        self.fx_nodes["makeSound"]=1001
        
        for name, fx in FxList.items():
            msg = OSCMessage("/s_new")
            packet = [fx.node_name, fx.node_id, 1, 1]

            self.fx_nodes[name] = fx.node_id
            
            msg.append( packet )
            bundle.append(msg)
        self.client.send(bundle)
        self.fx_setup_done = True
        return       

    def sendPlayerMessage(self, synthdef, packet, effects):
        if not self.fx_setup_done:
            self.fx_setup()
        # Create a bundle
        bundle = OSCBundle()
        this_node = self.nextnodeID()
        this_bus  = self.nextbusID()

        # Synth
        msg = OSCMessage("/s_new")
        packet = [synthdef, this_node, 1, 1, 'bus', this_bus] + packet
        # packet = [synthdef, this_node, 1, 1] + packet
        msg.append( packet )
        bundle.append(msg)

        # Effects
        for fx in effects:
            this_node, last_node = self.fx_nodes[fx], this_node
            
            # Set control values
            msg = OSCMessage("/n_set")
            packet = [this_node] + effects[fx]
            msg.append( packet )
            bundle.append(msg)

            # Put after synth
            msg = OSCMessage("/n_after")
            packet = [this_node, last_node]
            msg.append( packet )
            bundle.append(msg)
            
        # Output
        this_node, last_node = self.fx_nodes['makeSound'], this_node

        # Control values
        msg = OSCMessage("/n_set")
        packet = [this_node, 'bus', this_bus]
        msg.append( packet )
        bundle.append(msg)

        # Put after effects
        msg = OSCMessage("/n_after")
        packet = [this_node, last_node]
        msg.append( packet )
        bundle.append(msg)

        print bundle

        # Send
        self.client.send( bundle )
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

            files = [FOXDOT_OSC_FUNC, FOXDOT_BUFFERS_FILE, FOXDOT_EFFECTS_FILE]
            files = files + GET_SYNTHDEF_FILES() + GET_ENVELOPE_FILES()

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

        
