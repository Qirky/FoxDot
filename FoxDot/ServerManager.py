"""
    ServerManager.py

    Handles OSC messages being sent to SuperCollider. Will try and
    read data from Settings/server.txt which should contain the IP
    address and port separated by a single space. If not it defaults
    to SuperCollider's defaults.

"""

from OSC import *


try:

    with open("Settings/server_address.txt") as f:
        info = f.readlines()[0].split()
        
    ADDRESS, PORT = (str(info[0]), int(info[1]))
    
except:
    
    ADDRESS, PORT = "localhost", 57110


class ServerManager:

    def __init__(self, addr=ADDRESS, port=PORT):

        self.addr = addr
        self.port = port

        self.client = OSCClient()
        self.client.connect( (self.addr, self.port) )        

        self.node = 1000

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

    def bufferRead(self, bufnum, path):
        message = OSCMessage("/b_allocRead")
        message.append([bufnum, path])
        self.client.send( message )
        return


class SCLangManager(ServerManager):
    def __init__(self, addr=ADDRESS, port=PORT+10):
        ServerManager.__init__(self, addr, port)
    def sendsclang(self, code, cmd='/foxdot'):
        msg = OSCMessage()
        msg.setAddress(cmd)
        msg.append(code)
        self.client.send(msg)
        return
