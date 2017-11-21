""" Handles OSC messages being sent to SuperCollider.
"""

from __future__ import absolute_import, division, print_function

import os
import subprocess
import sys

from time import sleep

from .Settings import *
from .Code import WarningMsg

if sys.version_info[0] > 2:
    from .OSC3 import *
else:
    from .OSC import *
    

class SCLangClient(OSCClient):
    def send(*args, **kwargs):
        try:
            OSCClient.send(*args, **kwargs)
        except Exception as e:
            print(e)

# TODO -- Create an abstract base class that could be sub-classed for users who want to send their OSC messages elsewhere

class ServerManager(object):
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.client = SCLangClient()
        self.client.connect( (self.addr, self.port) )
    @staticmethod
    def create_osc_msg(dictionary):
        """ Converts a Python dictionary into an OSC style list """
        msg = []
        for key, value in dictionary.items():
            msg += [key, value]
        return msg
    def sendOSC(self, message):
        return
    def get_bundle(self):
        return

class SCLangServerManager(ServerManager):

    fxlist    = None
    synthdefs = None

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
        self.bus  = 4

        self.fx_setup_done = False
        self.fx_names = {}

        # Clear SuperCollider nodes if any left over from other session etc

        self.freeAllNodes()

        # Toggle debug in SuperCollider

        self.dumpOSC(0)

    def __str__(self):
        return "FoxDot ServerManager Instance -> {}:{}".format(self.addr, self.port)

    def __repr__(self):
        return str(self)

    def nextnodeID(self):
        """ Gets the next node ID to use in SuperCollider """
        self.node += 1
        return self.node

    def query(self):
        """ Prints debug status to SuperCollider console """
        self.client.send(OSCMessage("/status"))
        return

    def nextbusID(self):
        """ Gets the next SuperCollider bus to use """
        if self.bus > 100:
            self.bus = 4
        self.bus += 1
        return self.bus

    def sendOSC(self, packet):
        """ Compiles and sends an 's_new' OSC message for SuperCollider """
        message = OSCMessage("/s_new")
        node = packet[1] = self.nextnodeID()
        message.append(packet)
        self.client.send( message )   
        return

    def freeAllNodes(self):
        """ Triggers a free all message to kill all active nodes (sounds) in SuperCollider """
        msg = OSCMessage("/g_freeAll")
        msg.append([1])
        self.client.send(msg)
        return

    def setFx(self, fx_list):
        self.fxlist   = fx_list
        self.fx_names = {name: fx.synthdef for name, fx in fx_list.items() }
        return

    def get_midi_message(self, synthdef, packet):

        bundle.setAddress("/foxdot_midi")

        msg = OSCMessage()
        msg.setAddress("/foxdot_midi")

        note    = packet.get("midinote", 60)
        vel     = min(127, (packet.get("amp", 1) * 128) - 1)
        sus     = packet.get("sus", 0.5)
        channel = packet.get("channel", 0)

        msg.append( [synthdef.name, note, vel, sus, channel] )

        bundle.append(msg)

        return bundle


    def get_init_node(self, node, bus, group_id, synthdef, packet):
    
        msg = OSCMessage("/s_new")

        # Make sure messages release themselves after 8 * the duration at max (temp)
        
        max_sus = float(packet["sus"] * 8) # might be able to get rid of this
        
        key = "rate" if synthdef.name in (SamplePlayer, LoopPlayer) else "freq"
        
        if key in packet:
        
            value = ["rate", packet[key]]
        
        else:
        
            value = []
        
        osc_packet = ["startSound", node, 0, group_id, 'bus', bus, "sus", max_sus] + value
        
        msg.append( osc_packet )
        
        return msg, node

    def get_control_effect_nodes(self, node, bus, group_id, effects):

        pkg = []

        for fx in self.fxlist.order[0]:

            if fx in effects:

                this_effect = effects[fx]

                # Get next node ID
                node, last_node = self.nextnodeID(), node
            
                msg = OSCMessage("/s_new")
            
                osc_packet = [self.fx_names[fx], node, 1, group_id, 'bus', bus] + this_effect
            
                msg.append(osc_packet)
            
                pkg.append(msg)

        return pkg, node

    def get_synth_node(self, node, bus, group_id, synthdef, packet):
        
        msg = OSCMessage("/s_new")

        new_message = {}

        for key in packet:

            if key != "env":

                try:

                    new_message[key] = float(packet[key]) # is this not already the case?

                except TypeError as e:

                    WarningMsg( "Could not convert '{}' argument '{}' to float. Set to 0".format( key, packet[key] ))
                    new_message[key] = 0.0

        # Get next node ID
        node, last_node = self.nextnodeID(), node                
        
        osc_packet = [synthdef.name, node, 1, group_id, 'bus', bus] + self.create_osc_msg(new_message)        
        
        msg.append( osc_packet )

        return msg, node

    def get_pre_env_effect_nodes(self, node, bus, group_id,effects):

        pkg = []

        for fx in self.fxlist.order[1]:

            if fx in effects:

                this_effect = effects[fx]

                # Get next node ID
                node, last_node = self.nextnodeID(), node
                msg = OSCMessage("/s_new")
                osc_packet = [self.fx_names[fx], node, 1, group_id, 'bus', bus] + this_effect
                msg.append( osc_packet )
                pkg.append(msg)
    
        return pkg, node

    def get_synth_envelope(self, node, bus, group_id, synthdef, packet):

        env_packet = {  "sus" : packet["sus"],
                        "amp" : packet["amp"] }

        for key in ("atk", "decay", "rel", "legato", "curve", "gain"):

            # Try and get from the player

            value = packet.get(key, None)

            # If it is absent or set to None, get default from Synth

            if value is None:

                value = synthdef.get_default_env(key)

            # Store

            env_packet[key] = value

        env = synthdef.get_default_env("env") if packet.get("env", None) is None else packet.get("env", None)

        try:

            dest = env.get_env_name()

        except AttributeError as e:

            # Set the curve value

            env_packet["curve"] = env
            dest = "BasicEnvelope"

        node, last_node = self.nextnodeID(), node
        msg = OSCMessage("/s_new")
        osc_packet = [dest, node, 1, group_id, 'bus', bus] + self.create_osc_msg(env_packet)
        msg.append( osc_packet )

        return msg, node

    def get_post_env_effect_nodes(self, node, bus, group_id, effects ):

        pkg = []

        for fx in self.fxlist.order[2]:

            if fx in effects:

                this_effect = effects[fx]

                # Get next node ID
                node, last_node = self.nextnodeID(), node
                msg = OSCMessage("/s_new")
                osc_packet = [self.fx_names[fx], node, 1, group_id, 'bus', bus] + this_effect
                msg.append( osc_packet )
                pkg.append(msg)

        return pkg, node

    def get_exit_node(self, node, bus, group_id, packet):
        
        msg = OSCMessage("/s_new")
        node, last_node = self.nextnodeID(), node
        osc_packet = ['makeSound', node, 1, group_id, 'bus', bus, 'sus', float(packet["sus"] * 8)]
        msg.append( osc_packet )

        return msg, node

    def get_bundle(self, synthdef, packet, effects, timestamp=0):    

        # Get the actual synthdef object

        synthdef = self.synthdefs[synthdef]

        # Create a bundle
        
        bundle = OSCBundle(time=timestamp)

        # Create a specific message for midi

        if synthdef.name == "MidiOut": # this should be in a dict of synthdef to functions maybe? we need a "nudge to sync"

            return self.get_midi_message(synthdef, packet)

        # Create a group for the note
        group_id = self.nextnodeID()
        msg = OSCMessage("/g_new")
        msg.append( [group_id, 1, 1] )
        
        bundle.append(msg)

        # Get the bus and SynthDef nodes
        this_bus  = self.nextbusID()
        this_node = self.nextnodeID()

        # First node of the group (control rate)

        msg, this_node = self.get_init_node(this_node, this_bus, group_id, synthdef, packet)

        # Add effects to control rate e.g. vibrato        

        bundle.append( msg )

        pkg, this_node = self.get_control_effect_nodes(this_node, this_bus, group_id, effects)

        for msg in pkg:

            bundle.append(msg)

        # trigger synth

        msg, this_node = self.get_synth_node(this_node, this_bus, group_id, synthdef, packet)

        bundle.append(msg)

        # ORDER 1

        pkg, this_node = self.get_pre_env_effect_nodes(this_node, this_bus, group_id, effects)

        for msg in pkg:

            bundle.append(msg)

        # ENVELOPE

        # msg, this_node = self.get_synth_envelope(this_node, this_bus, group_id, synthdef, packet)

        # bundle.append( msg )

        # ORDER 2 (AUDIO EFFECTS)

        pkg, this_node = self.get_post_env_effect_nodes(this_node, this_bus, group_id, effects)
    
        for msg in pkg:
    
            bundle.append(msg)

        # OUT

        msg, _ = self.get_exit_node(this_node, this_bus, group_id, packet)

        bundle.append(msg)
        
        return bundle        

    def send(self, address, message):
        """ Sends message (a list) to SuperCollider """
        msg = OSCMessage(address)
        msg.append(message)
        self.client.send(msg)
        return

    def free_node(self, node):
        """ Sends a message to SuperCollider to stop a specific node """
        message = OSCMessage("/n_free")
        message.append(node)
        self.client.send( message )
        return

    def bufferRead(self, path, bufnum):
        """ Sends a message to SuperCollider to read an audio file into a buffer """
        message = OSCMessage("/b_allocRead")
        message.append([bufnum, path])
        self.client.send( message )
        return

    def sendMidi(self, msg, cmd="/foxdot_midi"):
        """ Sends a message to the FoxDot class in SuperCollider to forward a MIDI message """
        msg.setAddress(cmd)
        self.sclang.send(msg)
        return

    def loadSynthDef(self, fn, cmd='/foxdot'):
        """ Sends a message to the FoxDot class in SuperCollider to load a SynthDef from file """
        msg = OSCMessage()
        msg.setAddress(cmd)
        msg.append(fn)
        self.sclang.send(msg)
        return

    def dumpOSC(self, value=1):
        """ Debug - Dumps OSC messages SCLang side """
        msg = OSCMessage("/dumpOSC")
        msg.append(value)
        self.client.send(msg)
        return

    def start(self):
        """ Boots SuperCollider using `subprocess`"""

        if not self.booted:
            
            os.chdir(SC_DIRECTORY)
            
            print("Booting SuperCollider Server...")

            self.daemon = subprocess.Popen([SCLANG_EXEC, '-D', FOXDOT_STARTUP_FILE])

            os.chdir(USER_CWD)

            self.booted = True

        else:
            
            print("Warning: SuperCollider already running")
            
        return

    def makeStartupFile(self):
        ''' Boot SuperCollider and connect over OSC '''

        # 1. Compile startup file

        with open(FOXDOT_STARTUP_FILE, 'w') as startup:

            startup.write('''Routine.run {
            s.options.blockSize = 128;
            s.options.memSize = 131072;
            s.bootSync();\n''')

            files = [FOXDOT_OSC_FUNC, FOXDOT_BUFFERS_FILE]
            files = files + GET_SYNTHDEF_FILES() + GET_FX_FILES()
            
            for fn in files:

                f = open(fn)
                startup.write(f.read())
                startup.write("\n\n")

            startup.write("};")

        return

    def quit(self):
        if self.booted:
            self.client.send(OSCMessage("/quit"))
            sleep(1)
            self.daemon.terminate()
        return

try:
    import socketserver

except ImportError:

    import SocketServer as socketserver

import socket
import json
from threading import Thread
from time import sleep

class Message:
    """ Wrapper for JSON messages sent to the server """
    def __init__(self, data):
        self.data = data
    def __str__(self):
        """ Prepares the json message to be sent with first 4 digits
            denoting the length of the message """
        packet = str(json.dumps(self.data, separators=(',',':')))
        length = "{:04d}".format( len(packet) )
        return length + packet
    def __len__(self):
        return len(str(self))
    def asString(self):
        return str(self)

def read_from_socket(sock):
    """ Reads data from the socket """
    # Get number single int that tells us how many digits to read
    try:
        bits = int(sock.recv(4).decode())
    except(ConnectionAbortedError, ConnectionResetError):
        return None
    if bits > 0:
        # Read the remaining data (JSON)
        data = sock.recv(bits).decode()
        # Convert back to Python data structure
        return json.loads(data)

def send_to_socket(sock, data):
    """ Converts Python data structure to JSON message and
        sends to a connected socket """
    msg = Message(data)
    # Get length and store as string
    msg_len, msg_str = len(msg), str(msg).encode()
    # Continually send until we know all of the data has been sent
    sent = 0
    while sent < msg_len:
        bits = sock.send(msg_str[sent:])
        sent += bits
    return

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ Base class """
    pass

class TempoServer(ThreadedServer):
    """ Used in TempoClock.py to connect to instances of FoxDot over a network. Sends
        bpm changes over the network. On initial request this sends the start_time value
        of the clock """

    def __init__(self, clock, port=57999):
        # tempo clock
        RequestHandler.metro = self.metro = clock

        # Address information
        self.hostname = str(socket.gethostname())

        # Listen on any IP
        self.ip_addr  = "0.0.0.0"
        self.port     = int(port)

        # Public ip for server is the first IPv4 address we find, else just show the hostname
        self.ip_pub = self.hostname
        
        try:
            for info in socket.getaddrinfo(socket.gethostname(), None):
                if info[0] == 2:
                    self.ip_pub = info[4][0]
                    break
        except socket.gaierror:
            pass

        # Instantiate server process

        ThreadedServer.__init__(self, (self.ip_addr, self.port), RequestHandler)
        self.server_thread = Thread(target=self.serve_forever)
        self.server_thread.daemon = False
        self.running = False

    def __str__(self):
        return "{} on port {}\n".format(self.ip_pub, self.port)

    def start(self):
        """ Starts listening on the socket """

        self.running = True
        self.server_thread.start()

        return

    def kill(self):
        """ Properly terminates the server instance """
        self.running = False
        self.server_thread.join(0)
        self.shutdown()
        self.server_close()
        return

class RequestHandler(socketserver.BaseRequestHandler):
    """ Created whenever a new connection to the server is made:
        self.request = socket
        self.server  = Server instance
        self.client_address = (address, port)
    """

    def handle(self):
        """ Overload """
        while True:

            data = read_from_socket(self.request)           

            if data is None:

                print("Client disconnected from {}".format(self.client_address))

                break

            else:

                # Get the requested data and send to client

                new_data = {}
                
                for item in data["request"]:

                    new_data[item] = self.metro.get_attr(item)

                send_to_socket(self.request, new_data)
            
        return

class TempoClient:
    def __init__(self, clock):
        self.metro = clock

        self.server_hostname = None
        self.server_port     = None
        self.server_address  = None
        
        self.socket   = None

    def connect(self, hostname, port=57890):
        """ Connects to the server instance """

        # Get details of remote
        self.server_hostname = hostname
        self.server_port     = int(port)
        self.server_address  = (self.server_hostname, self.server_port)

        # Connect to remote

        try:

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.socket.connect(self.server_address)

        except Exception as e:

            raise(e)

            raise(ConnectionError("Could not connect to host '{}'".format( self.server_hostname ) ) )

        # connect to the server and listen for new updates for the tempo-clock

        self.listening = True
        self.daemon = Thread(target=self.listen)
        self.daemon.start()

        self.send({"request" : ["bpm", "start_time"]})
        
        return self

    def send(self, data):
        """ Sends data to server """
        return send_to_socket(self.socket, data)

    def listen(self):
        """ Listens out for data coming from the server and passes it on
            to the handler.
        """
        while self.listening:
            data = read_from_socket(self.socket)
            if data is None:
                break
            for key, value in data.items():
                self.metro.set_attr(key, value)
        return      

    def kill(self):
        """ Properly terminates the connection to the server """
        self.listening = False
        self.socket.close()
        return


if __name__ != "__main__":

    from .Settings import ADDRESS, PORT, PORT2

    DefaultServer = SCLangServerManager(ADDRESS, PORT, PORT2)