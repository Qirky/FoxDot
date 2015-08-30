# Server Manager
from OSC import *

client = OSCClient()
client.connect( ("localhost", 57110) )

class ServerManager:

    def __init__(self):
        self.node = 1000

        message = OSCMessage("/dumpOSC")
        message.append(1)
        #client.send( message )

    def nextnodeID(self):

        # After xx nodes, we start to free

        xx = 50

        #if self.node >= 1000 + xx:

        #    self.free_node( self.node - xx )
        
        self.node += 1

        return self.node

    def play_note(self, packet):
        message = OSCMessage("/s_new")
        packet[1]  = self.nextnodeID()
        message.append(packet)
        client.send( message )

    def send(self, message):
        client.send(OSCMessage(message))

    def free_node(self, node):

        message = OSCMessage("/n_free")
        message.append(node)
        client.send( message )
