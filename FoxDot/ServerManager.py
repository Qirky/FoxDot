"""
    ServerManager.py

    Handles OSC messages being sent to SuperCollider.

"""

import os, socket
from OSC import *
from subprocess import Popen
from time import sleep


class SCLangServerManager:

    def __init__(self, addr, osc_port, sclang_port):

        self.addr = addr
        self.port = osc_port
        self.SCLang_port = sclang_port

        self.booted = False
        self.wait_time = 5
        self.count = 0
        
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
        """ Don't use """

        self.count += 1

        if not self.booted:
            
            conf = os.path.realpath(FOXDOT_ROOT + OSC_FUNC)
            
            os.chdir(SC_DIRECTORY)
            
            print("Booting SuperCollider Server...")
            
            self.daemon = Popen([SCLANG_EXEC, '-D', conf])

            sleep(self.wait_time)

            os.chdir(USER_CWD)

            self.booted = True

        else:
            
            print("Warning: SuperCollider already running")
            
        return

    def quit(self):
        if self.booted:
            self.client.send(OSCMessage("/quit"))
            sleep(0.5)
            self.daemon.terminate()
        return

#================================#
#     Realtime Collaboration     #
#================================#

import socket
import SocketServer
import re
from threading import Thread
from Code import execute as ex

re_msg = re.compile(r"(.*?)@(.*?)@(.*?)@(.*)", re.DOTALL)

class NetworkMessage:
    def __init__(self, string):
        data = re_msg.match(string)
        self.raw_string = string
        if data:

            self.head, self.hostname, self.port, self.message = data.groups()

            self.port = int(self.port)
            
        else:

            self.head = None
            self.hostname = None
            self.port = None
            self.message = None
            
        self.address = (self.hostname, self.port)            

class FoxDotServerHandler(SocketServer.BaseRequestHandler):
    master = None
    def handle(self):
        """ self.request = socket
            self.server  = ThreadedServer
            self.client_address = (address, port)
        """
        while self.master.running:
            
            # Read from client
            msg = NetworkMessage(self.request.recv(4096))

            # If data starts with NEW_PEER@ we add to peers

            if msg.head == "NEW_PEER":
                
                # Add new peer
                new_peer = FoxDotClient(msg.hostname, msg.port)

                # Tell new peer to set all text to Master

                if msg.address != self.master.peer.address:

                    print "New connection from {} {}\n".format(*msg.address)
                    
                    new_peer.update_text(self.master.peer.widget.get_all())

                # Tell existing peers about new peer and vice versa

                for peer in self.master.peers:

                    peer.add_peer(msg.address)

                    new_peer.add_peer_info(peer)

                # Add to master list

                self.master.peers.append(new_peer)
                
            elif msg.head == "PUSH":

                # Else we send to all peers the same messsage

                for peer in self.master.peers:

                    # Don't send keystroke back to the sender

                    if msg.address != peer.address:

                        # Send the keystroke instruction to all other peers

                        peer.send(msg.raw_string)

            else:

                print "Bad string", msg.raw_string
        return

class PeerHandler(SocketServer.BaseRequestHandler):
    """ Class for handling messages sent to the peers from
        the server and updating the GUI.

        Types of message:

        - SET_ALL
        - NEW_PEER
        - PULL_PEER
        - PUSH
    """
    master = None
    def handle(self):
        while self.master.running:
            msg = NetworkMessage(self.request.recv(4096))
            if msg.head == "SET_ALL":

                # "Set all" messages need have

                #   - The text to update the GUI with

                self.master.widget.set_all(msg.message)
                self.master.widget.root.event_generate("<Control-Home>")

            elif msg.head == "PULL_PEER":
            
                #   - Names of peers and their row/column co-ordinates

                hostname, port, name, line, column = msg.message.split()
                new_peer = PeerProxy((hostname, int(port)), name)
                new_peer.line = int(line)
                new_peer.column = int(column)
                self.master.peers.append(new_peer)
                
            elif msg.head == "PUSH":

                # Push message needs to have:

                #   - Peer address
                #   - Peer name (hostname by default)
                #   - The keystroke
                #   - The index where the keystroke took place
    
                self.master.widget.peer_key_press(msg.message)

            elif msg.head == "NEW_PEER":

                # "New peer message" needs to have
                
                #   - The name and address of that peer
                #   - By default, new peers cursor set to 1.0

                pass


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class FoxDotServer:
    """
        This the master Server instance. Other peers on the
        network connect to it and send their keypress information
        to the server, which then sends it on to the others
    """
    def __init__(self, hostname=socket.gethostname(), port=57890, boot=True):
        self.hostname = hostname
        self.port     = port
        self.address  = (self.hostname, self.port)
        
        self.server   = ThreadedServer(self.address, FoxDotServerHandler)

        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.running = False
        
        # peers is a list of clients (including this machine)
        self.peer = Peer(self.hostname, self.port + 1)
        self.peers = []

        # Give handler information about this server
        FoxDotServerHandler.master = self

        if boot: self.boot()

    def boot(self):
        self.server_thread.start()
        self.running = True
        # Connect the local peer to this server
        self.peer.connect(*self.address)
        print "Server running on port {}\n".format(self.port)
        return

    def kill(self):
        self.running = False
        self.server.shutdown()
        self.server.server_close()
        return
    

class FoxDotClient: # Represent the connected machines
    def __init__(self, host, port):
        self.hostname = host
        self.port = int(port)
        self.address = (self.hostname, self.port)
        self.conn = socket.socket()
        self.conn.connect(self.address)
        self.message  = "{}" + "@{}@{}@".format(self.hostname, self.port) + "{}"

        self.name = None # Peer identifier
        self.line = 0
        self.column = 0
        
    def __str__(self):
        return "{}:{}".format(*self.address)
    def send(self, string):
        self.conn.sendall(string)
    def push_message(self, index, string):
        self.conn.sendall(self.message.format("PUSH", string))
    def update_text(self, text):
        """ Sends a SET_ALL message with the contents of the window """
        self.conn.sendall(self.message.format("SET_ALL", text))
    def add_peer(self, address):
        self.conn.sendall(self.message.format("NEW_PEER", "{} {}".format(*address)))
    def add_peer_info(self, client):
        self.conn.sendall(self.message.format("PULL_PEER", "{} {} {} {} {}".format(client.hostname, client.port, client.name, client.line, client.column)))
        
        

class Peer: # These sit on non-master machines
    """
        Listens for messages from a remote FoxDot Server instance
        and send keystroke data

    """
    def __init__(self, hostname=socket.gethostname(), port=57891, name=None):
        self.hostname = hostname
        self.port     = port
        self.address  = (self.hostname, self.port)
        self.server   = ThreadedServer(self.address, PeerHandler)
        self.message  = "{}" + "@{}@{}@".format(self.hostname, self.port) + "{}"

        self.name     = None

        # List of other peers on the network

        self.peers = []

        PeerHandler.master = self

        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.running = False

        sock = socket.socket()
        self.conn = None

        self.connected=False
        
        self.widget       = ex.namespace['FoxDot']
        self.widget.peers = self.peers
        self.widget.peer  = self

    def connect(self, hostname, port=57890):
        """ Connects to the master FoxDot server and
            start a listening instance on this machine """
        if not self.connected:
            # Connect to remote
            self.conn = socket.socket()
            self.conn.connect((hostname, port))
            self.conn.sendall(self.message.format("NEW_PEER", "{} {}".format(*self.address)))
            # Launch local
            self.server_thread.start()
            self.running = True
            self.connected=True
            self.widget.network = True
        return

    def push(self, *args):
        self.conn.sendall(self.message.format("PUSH", " ".join(args)))
        return

    def update_peers(self, update_message):
        self.peers =  []
        for p in update_message.split("@"):
            if p:
                p = p.split("--")
                host, port = p[:2]
                new_peer = PeerProxy((host, port))
                if len(p) > 2:
                    new_peer.name = p[2]
                self.peers.append(new_peer)
        return

class PeerProxy:
    def __init__(self, address, name=None):
        self.hostname = address[0]
        self.port     = address[1]
        self.name     = name if name is not None else self.hosname
        self.line     = 0
        self.column   = 0

if __name__ != "__main__":

    from Settings import ADDRESS, PORT, PORT2

    Server = SCLangServerManager(ADDRESS, PORT, PORT2)
