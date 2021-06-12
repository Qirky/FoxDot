""" Handles OSC messages being sent to SuperCollider.
"""
from __future__ import absolute_import, division, print_function
import sys

if sys.version_info[0] > 2:
    import queue
else:
    import Queue as queue

import json
import socket
import sys
import threading
import time
import itertools
import os.path

from collections import namedtuple
from threading import Thread

from .Code import WarningMsg
from .Settings import *

if sys.version_info[0] > 2:
    from .OSC3 import *
else:
    from .OSC import *

# Keep in sync with Info.scd
ServerInfo = namedtuple(
    'ServerInfo',
    ('sample_rate', 'actual_sample_rate', 'num_synths', 'num_groups',
     'num_audio_bus_channels', 'num_control_bus_channels',
     'num_input_bus_channels', 'num_output_bus_channels', 'num_buffers',
     'max_nodes', 'max_synth_defs', 'foxdot_root', 'foxdot_snd'))


class OSCClientWrapper(OSCClient):
    error_printed=False
    def send(*args, **kwargs):
        """ Sends the message given but prints errors instead of raising them """
        try:
            OSCClient.send(*args, **kwargs)
        except OSCClientError as e:
            if not OSCClientWrapper.error_printed:
                print("Error sending message to SuperCollider server instance: make sure FoxDot quark is running and try again.")
                OSCClientWrapper.error_printed = True


class OSCConnect(OSCClientWrapper):
    """ An OSCClientWrapper that connects on initialisation """
    def __init__(self, address):
        OSCClientWrapper.__init__(self)
        self.connect(address)


class RequestTimeout(Exception):
    """ Raised if expecting a response from the server but received none """


class BidirectionalOSCServer(OSCServer):
    """
    This is a combination client/server

    The UDP server is necessary for receiving responses from the SCLang server
    when we query it with requests.

    Note that this is not thread-safe, as the receive() method can discard messages
    """
    def __init__(self, server_address=('localhost', 0), client=None, return_port=0):
        OSCServer.__init__(self, server_address, client, return_port)
        self._server_thread = None
        self.addDefaultHandlers()
        self.addMsgHandler('default', self._handle_message)
        self._response_queue = queue.Queue()
        self._printed_error = False

    def connect(self, addr):
        """ Connect to an address and start the server thread """
        self.client.connect(addr)
        self.start()

    def start(self):
        """ Start the server thread. """
        if self._server_thread is not None:
            return
        self._server_thread = threading.Thread(target=self.serve_forever)
        self._server_thread.setDaemon(True)
        self._server_thread.start()

    def stop(self):
        """ Stop the server thread and close the socket. """
        if self._server_thread is None:
            return
        self.running = False
        self._server_thread.join()
        self.server_close()

    def _handle_message(self, addr, tags, data, client_address):
        self._response_queue.put((addr, data))

    def send(self, *args, **kwargs):
        try:
            self.client.send(*args, **kwargs)
        except OSCClientError as e:
            if not self._printed_error:
                print("Error: No connection made to SuperCollider server instance.")
                self._printed_error = True

    def receive(self, pattern, timeout=2):
        """
        Retrieve the first message matching the pattern

        All messages received that do not match will be discarded
        """
        expr = getRegEx(pattern)
        now = start = time.time()
        while now - start < timeout:
            try:
                addr, data = self._response_queue.get(True, start + timeout - now)
            except queue.Empty:
                raise RequestTimeout()
            if type(addr) is bytes:
                addr = addr.decode()
            match = expr.match(addr)
            if match and (match.end() == len(addr)):
                return data
            now = time.time()

#  Create an abstract base class that could be sub-classed for users who want to send their OSC messages elsewhere

class ServerManager(object):
    def __init__(self, addr, port, osc_address="/s_new"):
        self.addr = addr
        self.port = port
        self.client = OSCClientWrapper()
        self.client.connect( (self.addr, self.port) )
        self.osc_address = osc_address

        self.node = 1000
        self.num_input_busses = 2
        self.num_output_busses = 2
        self.bus = self.num_input_busses + self.num_output_busses
        self.max_busses = 100
        self.max_buffers = 1024

    @staticmethod
    def create_osc_msg(dictionary):
        """ Converts a Python dictionary into an OSC style list """
        msg = []
        for key, value in dictionary.items():
            msg += [key, value]
        return msg

    def sendOSC(self, osc_message):
        self.client.send( osc_message )
        return

    def get_bundle(self, *args, **kwargs):
        bundle  = OSCBundle(time=kwargs.get("timestamp", 0))
        message = OSCMessage(self.osc_address)
        for item in args:
            if type(item) == dict:
                message.append(self.create_osc_msg(item))
            else:
                message.append(item)
        bundle.append(message)
        return bundle

    def loadSynthDef(self, *args, **kwargs):
        return
    def setFx(self, *args, **kwargs):
        return

class SCLangServerManager(ServerManager):

    fxlist    = None
    synthdefs = None

    def __init__(self, addr, osc_port, sclang_port, foxdot_root, foxdot_snd):

        self.addr = addr
        self.port = osc_port
        self.SCLang_port = sclang_port
        self.foxdot_root = foxdot_root
        self.foxdot_snd = foxdot_snd
        self.foxdot_root_remote = ""
        self.foxdot_snd_remote = ""

        self.midi_nudge = 0

        self.booted = False
        self.wait_time = 5
        self.count = 0

        # Assign a valid OSC Client
        self.forward = None

        self.node = 1000
        self.num_input_busses = 2
        self.num_output_busses = 2
        self.bus = self.num_input_busses + self.num_output_busses
        self.max_busses = 100
        self.max_buffers = 1024

        self.fx_setup_done = False
        self.fx_names = {}

        self.reset()

    def reset(self):

        # General SuperCollider OSC connection
        self.client = OSCClientWrapper()
        self.client.connect( (self.addr, self.port) )

        # OSC Connection for custom OSCFunc in SuperCollider
        if GET_SC_INFO:
            # Prevent SocketError when connecting to a remote FoxDot instance
            server_address=('0.0.0.0', 0)
            if (self.addr == 'localhost' or self.addr == '127.0.0.1'):
                server_address=('localhost', 0)

            self.sclang = BidirectionalOSCServer(server_address=server_address)
            self.sclang.connect( (self.addr, self.SCLang_port) )
            self.loadSynthDef(FOXDOT_INFO_FILE)
            try:
                info = self.getInfo()
            except RequestTimeout:
                # It's not terrible if we couldn't fetch the info, but we should log it.
                WarningMsg("Could not fetch info from SCLang server. Using defaults...")
            else:
                self.max_buffers = info.num_buffers
                self.num_input_busses = info.num_input_bus_channels
                self.num_output_busses = info.num_output_bus_channels
                self.max_busses = info.num_audio_bus_channels
                self.bus = self.num_input_busses + self.num_output_busses
                self.foxdot_root_remote = info.foxdot_root
                self.foxdot_snd_remote = info.foxdot_snd
        else:
            self.sclang = OSCClientWrapper()
            self.sclang.connect( (self.addr, self.SCLang_port))

        # Clear SuperCollider nodes if any left over from other session etc

        self.freeAllNodes()

        # Load recorder OSCFunc

        self.loadRecorder() # move to the quark?

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
        self.bus += 2
        # Make sure we still have 2 audio channels available
        if self.bus + 1 >= self.max_busses:
            self.bus = self.num_input_busses + self.num_output_busses
        return self.bus

    def sendOSC(self, osc_message):
        """ Sends an OSC message to the server. Checks for midi messages """
        
        if osc_message.address == OSC_MIDI_ADDRESS:
        
            self.sclang.send( osc_message )
        
        else:
        
            self.client.send( osc_message )
        
        # If we are sending other messages as well
        
        if self.forward is not None:
            
            self.forward.send(osc_message)
        
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

    def set_midi_nudge(self, value):
        self.midi_nudge = value
        return

    def get_midi_message(self, synthdef, packet, timestamp):
        """ Prepares an OSC message to trigger midi sent from SuperCollider """

        bundle = OSCBundle(time=timestamp)
        bundle.setAddress(OSC_MIDI_ADDRESS) # these need to be variable names at least

        msg     = OSCMessage(OSC_MIDI_ADDRESS)

        note    = packet.get("midinote", 60)
        vel     = min(127, (packet.get("amp", 1) * 128) - 1)
        sus     = packet.get("sus", 0.5)
        channel = packet.get("channel", 0)
        nudge   = self.midi_nudge

        msg.append( [synthdef, note, vel, sus, channel, nudge] )

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

    def get_control_effect_nodes(self, node, bus, group_id, packet):

        pkg = []

        # Go through effects and put together with child attributes

        for fx in self.fxlist.order[0]:

            if fx in packet and packet[fx] != 0:

                # this_effect = effects[fx] # old pre-prepared

                # prepare each effect here

                this_effect = self.prepare_effect(fx, packet)

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

            if key not in ("env", "degree"): # skip some attr

                try:

                    new_message[key] = float(packet[key]) # is this not already the case?

                except (TypeError, ValueError) as e:

                    WarningMsg( "Could not convert '{}' argument '{}' to float. Set to 0".format( key, packet[key] ))
                    new_message[key] = 0.0

        # Get next node ID

        node, last_node = self.nextnodeID(), node

        osc_packet = [synthdef.name, node, 1, group_id, synthdef.bus_name, bus] \
            + self.create_osc_msg(new_message)

        msg.append( osc_packet )

        return msg, node

    def get_pre_env_effect_nodes(self, node, bus, group_id, packet):

        pkg = []

        for fx in self.fxlist.order[1]:

            if fx in packet and packet[fx] != 0:

                this_effect = self.prepare_effect(fx, packet)

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

    def get_post_env_effect_nodes(self, node, bus, group_id, packet):

        pkg = []

        for fx in self.fxlist.order[2]:

            if fx in packet and packet[fx] != 0:

                this_effect = self.prepare_effect(fx, packet)

                # Get next node ID
                node, last_node = self.nextnodeID(), node
                msg = OSCMessage("/s_new")
                osc_packet = [self.fx_names[fx], node, 1, group_id, 'bus', bus] + this_effect
                msg.append( osc_packet )
                pkg.append(msg)

        return pkg, node

    def prepare_effect(self, name, packet):
        """ Finds the child attributes in packet and returns an OSC style list """
        data   = []
        effect = self.fxlist[name]
        for key in effect.args:
             data.append(key)
             data.append(float(packet.get(key, effect.defaults[key])))
        return data

    def get_exit_node(self, node, bus, group_id, packet):
        
        msg = OSCMessage("/s_new")
        node, last_node = self.nextnodeID(), node
        osc_packet = ['makeSound', node, 1, group_id, 'bus', bus, 'sus', float(packet["sus"])]
        msg.append( osc_packet )

        return msg, node

    def get_bundle(self, synthdef, packet, timestamp=0):
        """ Returns the OSC Bundle for a notew based on a Player's SynthDef, and event and effects dictionaries """ 

        # Create a specific message for midi

        if synthdef == "MidiOut": # this should be in a dict of synthdef to functions maybe? we need a "nudge to sync"

            return self.get_midi_message(synthdef, packet, timestamp)

        # Create a bundle
        
        bundle = OSCBundle(time=timestamp)

        # Get the actual synthdef object

        synthdef = self.synthdefs[synthdef]

        # Create a group for the note
        group_id = self.nextnodeID()
        msg = OSCMessage("/g_new")
        msg.append( [group_id, 1, 1] )
        
        bundle.append(msg)

        # Get the bus and SynthDef nodes
        this_bus  = self.nextbusID()
        this_node = self.nextnodeID()

        # synthdef.preprocess_osc(packet) # so far, just "balance" to multiply amp by 1

        # First node of the group (control rate)

        msg, this_node = self.get_init_node(this_node, this_bus, group_id, synthdef, packet)

        # Add effects to control rate e.g. vibrato        

        bundle.append( msg )

        pkg, this_node = self.get_control_effect_nodes(this_node, this_bus, group_id, packet)

        for msg in pkg:

            bundle.append(msg)

        # trigger synth

        msg, this_node = self.get_synth_node(this_node, this_bus, group_id, synthdef, packet)

        bundle.append(msg)

        # ORDER 1

        pkg, this_node = self.get_pre_env_effect_nodes(this_node, this_bus, group_id, packet)

        for msg in pkg:

            bundle.append(msg)

        # ENVELOPE

        # msg, this_node = self.get_synth_envelope(this_node, this_bus, group_id, synthdef, packet)

        # bundle.append( msg )

        # ORDER 2 (AUDIO EFFECTS)

        pkg, this_node = self.get_post_env_effect_nodes(this_node, this_bus, group_id, packet)
    
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
        
        # If we are sending other messages as well
        
        if self.forward is not None:
        
            self.forward.send(message)
        
        return

    def free_node(self, node):
        """ Sends a message to SuperCollider to stop a specific node """
        message = OSCMessage("/n_free")
        message.append(node)
        self.client.send( message )
        return

    def bufferRead(self, path, bufnum):
        """ Sends a message to SuperCollider to read an audio file into a buffer """

        # Update path for proper file load in the remote Supercollider
        if (not(self.addr == 'localhost' or self.addr == '127.0.0.1')):
            path = path.replace(self.foxdot_snd, self.foxdot_snd_remote)

        message = OSCMessage("/b_allocRead")
        message.append([bufnum, path])
        self.client.send( message )
        return

    def bufferFree(self, bufnum):
        """ Sends a message to SuperCollider to free a buffer """
        message = OSCMessage("/b_free")
        message.append([bufnum])
        self.client.send(message)

    def sendMidi(self, msg, cmd=OSC_MIDI_ADDRESS):
        """ Sends a message to the FoxDot class in SuperCollider to forward a MIDI message """
        msg.setAddress(cmd)
        self.sclang.send(msg)
        return

    def loadSynthDef(self, fn, cmd='/foxdot'):
        """ Sends a message to the FoxDot class in SuperCollider to load a SynthDef from file """

        # Update path for proper file load in the remote Supercollider
        if (not(self.addr == 'localhost' or self.addr == '127.0.0.1')):
            fn = fn.replace(self.foxdot_root, self.foxdot_root_remote)

        msg = OSCMessage()
        msg.setAddress(cmd)
        msg.append(fn)
        self.sclang.send(msg)
        return

    def loadRecorder(self):
        """ Loads an OSCFunc that starts/stops recording to a set path """
        self.loadSynthDef(FOXDOT_RECORD_FILE)
        self._is_recording = False
        return

    def record(self, fn=None):
        """ Starts recording audio from SuperCollider """

        if self._is_recording is False:

            if fn is None:
                
                fn = "{}.aiff".format(get_timestamp())
            
            path = os.path.join(RECORDING_DIR, fn)

            msg = OSCMessage('/foxdot-record')
            msg.append([1, path])
            self.sclang.send(msg)

            self._is_recording = True
        
        return

    def stopRecording(self):
        """ Stops recording audio from SuperCollider """
        if self._is_recording is True:
            
            msg = OSCMessage('/foxdot-record')
            msg.append([0, ""]) # flag to stop recording
            self.sclang.send(msg)
            
            self._is_recording = False
        
        return

    def loadCompiled(self, fn):
        """ Sends a message to SuperCollider to load a compiled SynthDef file """
        msg = OSCMessage()
        msg.setAddress('/d_load')
        msg.append(fn)
        self.client.send(msg)

    def dumpOSC(self, value=1):
        """ Debug - Dumps OSC messages SCLang side """
        msg = OSCMessage("/dumpOSC")
        msg.append(value)
        self.client.send(msg)
        return

    def dumpTree(self, group_id=0, flag=0):
        """ Server will print the node tree """
        msg = OSCMessage("/g_dumpTree")
        msg.append([group_id, flag])
        self.client.send(msg)

    def getInfo(self):
        """ Fetch info about the SCLang server """
        msg = OSCMessage()
        msg.setAddress('/foxdot/info')
        self.sclang.send(msg)
        info = ServerInfo(*self.sclang.receive('/foxdot/info'))
        return info

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
        if self._is_recording:
            self.stopRecording()
        return

    def add_forward(self, addr, port):
        self.forward = OSCClientWrapper()
        self.forward.connect( (addr, port) )

try:
    
    import socketserver

except ImportError:

    import SocketServer as socketserver


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
    except:
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
        RequestHandler.metro  = self.metro = clock
        RequestHandler.master = self

        # Address information
        self.hostname = str(socket.gethostname())

        # Listen on any IP
        self.ip_addr  = "0.0.0.0"
        self.port     = int(port)

        # Public ip for server is the first IPv4 address we find, else just show the hostname
        self.ip_pub = self.hostname
        
        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.ip_pub = s.getsockname()[0]
            s.close()

        except OSError:

            pass

        # Instantiate server process

        self.peers = []

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

    def update_tempo(self, source, bpm, bpm_start_beat, bpm_start_time):
        """ Sends information  to all connected peers about changing tempo """
        for peer in self.peers:
            if peer is not source:
                peer.update_tempo(bpm, bpm_start_beat, bpm_start_time)
        # Update the master clock tempo if receiving from another peer
        if source is not None:
            self.metro.update_tempo_from_connection(bpm, bpm_start_beat, bpm_start_time)
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
    master = None

    def handle(self):
        """ Overload """

        print("New connection from {}".format(self.client_address))

        # First we get latency

        data = read_from_socket(self.request)

        # Should be "init" message

        assert "init" in data

        send_to_socket(self.request, {"clock_time": time.time()}) # maybe time at a beat?

        self.master.peers.append(self)

        while True:

            data = read_from_socket(self.request)

            # If a client disconnects, remove and print message

            if data is None:

                return self.disconnect()

            else:

                # Get the requested data and send to client

                if "request" in data:

                    send_to_socket(self.request, self.metro.get_sync_info())

                # Tell server to update tempo and update clients

                elif "new_bpm" in data:

                    self.master.update_tempo(self, **data["new_bpm"])

                elif "latency":

                    send_to_socket(self.request, ["latency"])

        return

    def disconnect(self):
        """ Prints a message to the master clock and removes a reference to this client """
        print("Client disconnected from {}".format(self.client_address))
        self.master.peers.remove(self)
        return 0

    def update_tempo(self, bpm, bpm_start_beat, bpm_start_time):

        data = {
            "new_bpm" :
                {
                    "bpm" : bpm,
                    "bpm_start_time" : bpm_start_time,
                    "bpm_start_beat" : bpm_start_beat
            }
        }

        send_to_socket(self.request, data)

        return


class TempoClient:
    def __init__(self, clock):
        self.metro = clock

        self.sync_keys = ("bpm_start_beat", "bpm_start_time", "bpm")

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

        # Send init message
        self.start_time = None
        self.stop_time  = None
        self.latency    = None
        self.recording_latency = False

        send_to_socket(self.socket, ["init"])
        
        self.start_timing()

        return self

    def start_timing(self):
        """ Starts an internal timer for calculating latency """
        self.start_time = time.time()

    def stop_timing(self):
        """ Stops the internal timer and calculates latency  """
        self.stop_time = time.time()
        self.calculate_latency(self.start_time, self.stop_time)

    def calculate_latency(self, start, end):
        """ Returns (and stores) the latency using the start and end time to send a message to the master server"""
        self.latency = (end - start) * 0.5
        return self.latency

    def record_latency(self):
        self.start_timing()
        self.recording_latency = True
        self.send(["latency"])
        return

    def send(self, data):
        """ Sends data to server """
        return send_to_socket(self.socket, data)

    def listen(self):
        """ Listens out for data coming from the server and passes it on
            to the handler.
        """
        
        # First message is machine clock time

        time_data = read_from_socket(self.socket)

        self.stop_timing()

        # self.metro.calculate_nudge(time_data["clock_time"], self.stop_time, self.latency)
        self.metro.calculate_nudge(time_data["clock_time"], self.start_time, self.latency)
        
        # Enter loop

        while self.listening:
            
            data = read_from_socket(self.socket)

            # Might be recording latency

            if self.recording_latency:

                self.stop_timing()
                self.recording_latency = False
            
            if data is None:
                break
            
            if "sync" in data:

                for key in self.sync_keys:
                    if key in data["sync"]:
                        object.__setattr__(self.metro, key, data["sync"][key])

                self.metro.update_tempo_from_connection(**data["sync"])

                self.metro.flag_wait_for_sync(False)
            
            elif "new_bpm" in data:

                self.metro.update_tempo_from_connection(**data["new_bpm"])
        return

    def update_tempo(self, bpm, bpm_start_beat, bpm_start_time):
        """ Sends data to other connected FoxDot instances to update their tempo """
        data = {
            "new_bpm" :
                {
                    "bpm" : bpm,
                    "bpm_start_time" : bpm_start_time,
                    "bpm_start_beat" : bpm_start_beat
            }
        }
        return self.send(data)

    def kill(self):
        """ Properly terminates the connection to the server """
        self.listening = False
        self.socket.close()
        return


if __name__ != "__main__":

    from .Settings import ADDRESS, PORT, PORT2, FORWARD_PORT, FORWARD_ADDRESS, FOXDOT_ROOT, FOXDOT_SND

    # DefaultServer = SCLangServerManager(ADDRESS, PORT, PORT2)
    Server = SCLangServerManager(ADDRESS, PORT, PORT2, FOXDOT_ROOT, FOXDOT_SND)

    if FORWARD_PORT and FORWARD_ADDRESS:
        Server.add_forward(FORWARD_ADDRESS, FORWARD_PORT)
