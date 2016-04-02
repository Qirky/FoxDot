"""
    Copyright Ryan Kirkbride 2015

    This module contains the objects for Instrument Players (those that send musical
    information to SuperCollider) and Sample Players (those that send buffer IDs to
    playback specific samples located in the Samples directory).

"""

from os.path import dirname
from copy import deepcopy # used to copy player attr dicts to stop sending them to SC TODO

from Patterns import *
from Midi import *

from Scale import Scale

import Code
import Buffers
import Effects

_PLAYER_TYPE  = 0
_SYNTH_TYPE   = 1
_SAMPLES_TYPE = 2


##################### ROOT PLAYER OBJECT #####################

class _player:

    CREATED = False
    _TYPE = _PLAYER_TYPE

    def __init__( self, name ):

        self.SynthDef = name
        self.metro = None
        self.server = None
        self.quantise = False
        self.stopping = False
        self.stop_point = 0
        self.following = None        

        # Define any standard variables that are used in the OSC message (make sure they are in the attr dict)

        self.attr = {}

        self.dur    = self.attr['dur']      =  [0]
        self.root   = self.attr['root']     =  [0]
        self.degree = self.attr['degree']   =  [0]
        self.oct    = self.attr['oct']      =  [5]
        self.amp    = self.attr['amp']      =  [0.5]
        self.pan    = self.attr['pan']      =  [0]
        self.sus    = self.attr['sus']      =  [1]
        self.rate   = self.attr['rate']     =  [1]
        self.buf    = self.attr['buf']      =  [0]

        self.freq   = [0]

        # Dictionary to store any effect arguments

        self.fx = Effects.Handler(self)

        # Sets the clock off a beat amount

        self.off = 0
        self.old_off = 0

        # Modifiers
        
        self.reversing = False

        # Modifier dict
        
        self.modf = {}
        self.reset() # This method is used to 'reset' the modifiers

        # Keeps track of which note to play etc
        
        self.event_n   = 0

        # Used for checking clock updates
        
        self.old_dur = None
        self.isplaying = False

    # --- Startup methods

    def reset(self):
        self.modf = dict([(key, [0]) for key in self.attr])
        self.modf['amp'] = 0.5
        return self    

    def begin(self):
        self.metro.playing.append(self)
        self.update_clock()
        self.CREATED = True
        return

    # --- Update methods

    def update_dict(self):
        """ Update attr dict with Streams """
        for a in self.attr:
            self.attr[a] = asStream( self.__dict__[a] )
        return

    def update_clock(self):

        # Initial location is the offset (if any)

        next_step = int(self.off * self.metro.steps)

        self.event_n = 0

        count = 0

        # Go through each clock step

        for i, step in enumerate(self.metro):

            # If step should contain self

            if i == next_step:

                # Add self if not already there

                if self not in step:

                    # Add player to clock

                    self.metro.add2q(self, i)

                # Work out duration of the note

                if self._TYPE is _SYNTH_TYPE:

                    dur = modi(self.attr['dur'], count)

                elif self._TYPE is _SAMPLES_TYPE:
                    
                    dur = modi(self.attr['dur_val'], count)

                next_step += int(float(dur) * self.metro.steps)

                # Increase duration counter

                count += 1

                # Increase event counter until NOW

                if i < self.metro.now():

                    self.event_n += 1

            # If step shouldn't contain self, remove it if it is in there

            else:

                if self in step:

                    step.remove(self)

        self.old_dur = self.attr['dur']
        self.old_off = self.off
        
        if self._TYPE is _SAMPLES_TYPE:
            self.old_dur_val = self.dur_val

        return

    def update_state(self, isEvent=True):

        # Kill the player if stopping
        if self.stopping and self.metro.beat >= self.stop_point:
            self.kill()
        # Update the clock if the duration values have changed
        if self.dur_updated():
            self.pat_to_buf()
            self.update_clock()
        # Go to the next event
        else:
            self.event_n += ( int(isEvent) * self.direction() )

        # Calculate frequency 
        self.freq = self.calculate_freq()
    
        # Update dictionary to contain only streams
        self.update_dict()

        return
    
    def dur_updated(self):
        """ Returns true if the duration has changed since the last update """
        if self._TYPE is _SYNTH_TYPE:
            return self.attr['dur'] != self.old_dur or self.off != self.old_off
        if self._TYPE is _SAMPLES_TYPE:
            return self.attr['dur'] != self.old_dur or self.attr['dur_val'] != self.old_dur_val

    # --- Data methods

    def tupleN(self):
        """ Returns the length of the largest nested tuple in the attr dict """
        size = len(self.freq)
        for stream in self.attr.values() + self.modf.values():
            for value in asStream(stream):
                try:
                    if len(value) > size:
                        size = len(value)
                except:
                    pass

        return size

    # --- Methods for preparing and sending OSC messages to SuperCollider

    def now(self, attr, x=0):
        """ Calculates the values for each attr to send to the server at the current clock time """

        modifier_event_n = self.event_n

        # Get which instrument is leading

        if self.following and attr == 'degree':

            attr_value = self.following.now('degree')

        else:

            attr_value = modi(self.attr[attr], self.event_n + x)
        
        # If the attribute isn't in the modf dictionary, default to 0

        try:

            modf_value = modi(self.modf[attr], modifier_event_n + x)

        except:

            modf_value = 0

        try:

            # Amp is multiplied, not added

            if attr == "amp":

                value = attr_value * modf_value

            else:
        
                value = attr_value + modf_value

        except:

            value = attr_value
        
        return value

    def osc_message(self, index=0):
        """ Creates an OSC packet to play a SynthDef in SuperCollider """

        nodeID = 0

        message = [self.SynthDef, nodeID, 1, 1, 'freq', modi(self.freq, index)]

        for key in self.attr:

            if key not in ('freq', 'degree', 'following'):

                val = modi(self.now(key), index)

                if key == "sus":

                    val = val * self.metro.beat_dur()

                message += [key, float(val)]

        return message

    def osc_effect(self, effect):
        """ If there are any effects added, send them to the server. Sets the default sustain to twice the currently set sustain """

        nodeID = 0
        
        message = [effect, nodeID, 1, 1]

        if "sus" in message:

            pass

        else:

            message += ["sus", self.now("sus") * 2]

        for arg, val in self.fx[effect].items():

            message += [arg, val]

        return message

    def send(self):
        """ Sends the current event data to SuperCollder """

        # Create OSC Message and play
        
        for i in range(self.tupleN()):
            
            self.server.sendOSC( self.osc_message( i )  )

            # Add any effects
            
            for fx in self.fx:

                self.server.sendOSC( self.osc_effect( fx ) )

        return

    #: Methods for stop/starting players

    def kill(self):

        self.isplaying = False
        self.event_n = 0
        self.metro.playing.remove(self)
        for step in self.metro:
            if self in step:
                step.remove(self)
        
        return self

    def stop(self, N=0):
        
        """ Removes the player from the Tempo clock and changes its internal
            playing state to False in N bars time
            - When N is 0 it stops immediately"""

        self.stopping = True
        
        self.stop_point = self.metro.beat

        if N > 0:

            self.stop_point += self.metro.til_next_bar() + ((N-1) * self.metro.bar_length())

        return self

    def pause(self):

        self.isplaying = False

        return self

    def play(self):

        if self not in self.metro.playing:

            self.metro.playing.append(self)

        self.isplaying = True
        self.stopping = False

        return self

    def start(self):

        self.play()

        return self

    # --- Modifying functions

    def reverse(self):
        """ Sets flag to reverse streams """
        self.reversing = not self.reversing
        return self

    def direction(self):
        """ Returns 1 if self.event_n is increasing, and -1 if it is decreasing """
        if self.reversing:
            return -1
        else:
            return 1

    def every(self, n, cmd, *args):

        # Creates an expression unique to this object and function
        e = "'{0}'=='{0}' and '{1}'=='{1}'".format(cmd.__name__, id(self))

        self.metro.when(e, lambda: cmd(self), n)

        return self

    def strum(self, dur=0.025):
        """ Adds a delay to a Synth Envelope """
        x = self.tupleN()
        if x > 1:
            self.delay = asStream([tuple(a * dur for a in range(x))])
        else:
            self.delay = asStream(dur)
        return self 

    # Special object methods

    def __name__(self):
        for name, var in globals().items():
            if self == var:
                return name

    def __repr__(self):
        return "<Player ('%s')>" % self.SynthDef

    def __str__(self):
        return self.SynthDef

    def __setattr__(self, name, value):
        if self.CREATED and type(value) != str:
            self.attr[name] = value
        self.__dict__[name] = value
        return

    # Placeholder methods

    def pat_to_buf(self):
        return

    def calculate_freq(self):
        return [0]

##################### SYNTHESISER PLAYERS #####################

class synth_(_player):

    _TYPE = _SYNTH_TYPE

    def __init__(self, SynthDef, degree=[0], **kwargs):

        # Inherit key methods

        _player.__init__(self, SynthDef)

        # Update self with kwargs
        
        self.attr.update(kwargs)
        self.update_dict()
        self.reset()

    def update(self, SynthDef, degree=[0], **kwargs):
        """ Updates the values of this Player """

        setattr(self, "SynthDef", SynthDef)
        setattr(self, "degree", asStream(degree))

        for name, value in kwargs.items():
            setattr(self, name, value)

        if "sus" not in kwargs:
            setattr(self, "sus", self.dur)

        return self

    def calculate_freq(self):
        """ Uses the scale, octave, and degree to calculate the frequency values to send to SuperCollider """

        now = {}
        
        for attr in ('degree', 'oct'):

            now[attr] = self.now(attr)

            try:

                now[attr] = list(now[attr])

            except:

                now[attr] = [now[attr]]
                
        size = max( len(now['oct']), len(now['degree']) )

        f = []

        for i in range(size):
            midinum = midi( self.scale, modi(now['oct'], i), modi(now['degree'], i) , self.now('root') )
            f.append( miditofreq(midinum) )
        return f
    
    def lshift(self, n=1):
        self.event_n -= (n+1)
        return self

    def rshift(self, n=1):
        self.event_n += n
        return self

    def follow(self, lead):
        """ Takes a now object and then follows the notes """

        self.following = lead
        self.scale = lead.scale

        return self

    def solo(self):

        self.following = None

        return self

    def copy(self, player):

        """ Copies the attr dict of player to self """

        self.dur    = player.attr['dur']
        self.scale  = player.attr['scale']
        self.root   = player.attr['root']
        self.degree = player.attr['degree']
        self.oct    = player.attr['oct']
        self.amp    = player.attr['amp']
        self.pan    = player.attr['pan']
        self.sus    = player.attr['sus']
        self.rate   = player.attr['rate']
        self.pos    = player.attr['pos']
        self.buf    = player.attr['buf']

        return self

    def f(self, data):

        """ adds value to frequency modifier """

        if type(data) == int:

            data = [data]

        # Add to modulator

        self.modf['freq'] = circular_add(self.modf['freq'], data)

        return self

    def offbeat(self, beat_len=0.5):
        """ Adds a 0 amplitude note to the start of the player"""

        self.off = beat_len

        return self

    # Methods affecting other players - every n times, do a random thing?

    def bother(self, other):

        return self

    def stutter(self, n=4):
        """ repeats each value in each stream n times """

        # if n is a list, stutter each degree[i] by n[i] times

        self.degree = Stutter(self.degree, n)

        return self

    def __int__(self):
        return int(self.now('degree'))

    def __float__(self):
        return float(self.now('degree'))

    def __add__(self, data):
        """ Change the degree modifier stream """
        self.modf['degree'] = asStream(data)
        return self

    def __iadd__(self, data):
        """ Increment the degree modifier stream """
        self.modf['degree'] = circular_add(self.modf['degree'], asStream(data))
        return self

    def __sub__(self, data):
        """ Change the degree modifier stream """
        data = asStream(data)
        data = [d * -1 for d in data]
        self.modf['degree'] = data
        return self

    def __isub__(self, data):
        """ de-increment the modifier stream """
        data = asStream(data)
        data = [d * -1 for d in data]
        self.modf['degree'] = circular_add(self.modf['degree'], data)
        return self

    def __mul__(self, data):

        """ Multiplying an instrument player multiplies each amp value by
            the input, or circularly if the input is a list. The input is
            stored here and calculated at the update stage """

        if type(data) in (int, float):

            data = [data]

        self.modf['amp'] = asStream(data)

        return self

    def __div__(self, data):

        if type(data) in (int, float):

            data = [data]

        self.modf['amp'] = [1.0 / d for d in data]

        return self

    def __cmp__(self, other):
        if isinstance(other, _player):
            return int( self is not other ) * -1
        # Used for comparing to numbers etc
        if self.now('degree') > other:
            return 1
        if self.now('degree') < other:
            return -1
        if self.now('degree') == other:
            return 0


# ---------------------------------------------- #
# Class for for reading samples from buffers     # 
# ---------------------------------------------- #

# Table of characters to buffers

BufferManager = Buffers.BufferManager().load()

class samples_(_player):

    _TYPE = _SAMPLES_TYPE
    
    SPECIAL_CHARS = " []()"
    REST = SPECIAL_CHARS[0]

    def __init__(self, pat=' ', speed=[1], **kwargs):

        _player.__init__(self, "sample_player")

        # Degree is the string of characters
        self.degree  = pat
        self.old_degree = ""

        # Real value of each sample duration
        self.dur_val = self.attr['dur_val'] = self.old_dur_val = None

        # Set samples a little louder
        self.amp = self.attr['amp'] = 1

        self.attr.update(kwargs)
        self.update_dict()

    def update(self, degree=" ", **kwargs):
        """ Updates the values of this Player """

        setattr(self, "degree", degree)

        self.pat_to_buf()

        for name, value in kwargs.items():
            setattr(self, name, value)

        return self

    def pat_to_buf(self):

        self.attr['dur_val'] = self.dur_val = PRhythm(self.degree, self.dur)

        new_string = P().fromString(self.degree).string()

        buf = []

        for i, char in enumerate(new_string):
            # If the string starts with a rest, point to an empty buffer
            if i is 0 and char == self.REST:
                buf.append(0)
            # Any characters not in brackets or rest
            if char not in self.SPECIAL_CHARS:
                buf.append(BufferManager.symbols.get(char, 0))

        self.attr['buf'] = self.buf = buf

        return
        

    def __add__(self, data):

        if type(data) == int:

            self.amp = [a + data for a in self.amp]

            return self

        if type(data) == str:

            self.degree += data

        if type(data) == list:

            try:

                self.pat = ''.join(data)

            except:

                pass

        return self


    def __sub__(self, data):

        if type(data) == int:

            data = [data]

        data = [d * -1 for d in data]

         # Add to modifier

        self.modf['degree'] = circular_add(self.modf['degree'], data)

        return self

    def __mul__(self, data):

        # TODO Sync in the clock

        if type(data) in (int, float):

            data = [data]

        size_dur  = len(self.attr['dur'])
        size_sus  = len(self.attr['sus'])
        size_data = len(data)

        size_max = max( size_dur , size_sus, size_data)

        self.dur = [ 0 for x in range(size_max) ]
        self.sus = [ 0 for x in range(size_max) ]

        for i in range( size_max ):

            self.dur[i] = self.attr['dur'][i % size_dur] * (1.0 / data[i % size_data])
            self.sus[i] = self.attr['sus'][i % size_sus] * (1.0 / data[i % size_data])

        return self

    def __div__(self, data):

        if type(data) in (int, float):

            data = [data]

        size_dur  = len(self.attr['dur'])
        size_data = len(data)

        size_max = max( size_dur , size_data)

        self.dur = [ 0 for x in range(size_max) ]

        for i in range( size_max ):

            self.dur[i] = self.attr['dur'][i % size_dur] / (1.0 / data[i % size_data])

        return self

    def char(self, other=None):
        if other is not None:
            try:
                if type(other) == str and len(other) == 1: #char
                    return BufferManager.bufnum(self.now('buf')) == other
                raise TypeError("Argument should be a one character string")
            except:
                return False
        else:
            try:
                return BufferManager.bufnum(self.now('buf'))
            except:
                return None

    def coarse(self, n=3):
        self.grain=n
        return self

###### GROUP OBJECT

class group:

    def __init__(self, *args):

        self.players = args

    def __len__(self):
        return len(self.players)

    def __setattr__(self, name, value):
        try:
            for p in self.players:
                try:
                    setattr(p, name, value)
                except:
                    print "AttributeError: '%s' object has no attribute '%s'" % (str(p), name)
        except:
            self.__dict__[name] = value 
        return self

    def stop(self, n=0):
        for item in self.players:
            item.stop(n)
        return self

    def play(self):
        for item in self.players:
            item.play()
        return self

Group = group
