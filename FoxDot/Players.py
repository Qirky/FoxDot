"""
    Copyright Ryan Kirkbride 2015

    This module contains the objects for Instrument Players (those that send musical
    information to SuperCollider) and Sample Players (those that send buffer IDs to
    playback specific samples located in the Samples directory).

"""

from os.path import dirname

from Patterns import *
from Midi import *

from Scale import Scale

import Code
import Buffers

_PLAYER_TYPE  = 0
_SYNTH_TYPE   = 1
_SAMPLES_TYPE = 2


##################### ROOT PLAYER OBJECT #####################

class PLAYER(Code.LiveObject):

    _VARS = []
    _INIT = False
    _TYPE = _PLAYER_TYPE
    _DUR  = 'dur'

    def __init__( self, name ):

        self.SynthDef = name
        self.metro = None
        self.server = None
        self.quantise = False
        self.stopping = False
        self.stop_point = 0
        self.following = None

        # Modifiers
        
        self.reversing = False
        self.when_statements = []

        # Keeps track of which note to play etc

        self.event_index = 0
        self.event_n = 0
        self.event = {}

        # Used for checking clock updates
        
        self.old_dur = None
        self.isplaying = False
        self.isAlive = True
        self.last_offset = 0

        # These dicts contain the attribute and modifier values that are sent to SuperCollider

        self.attr = {}
        self.modf = {}
        
        # List the internal variables we don't want to send to SuperCollider

        self._VARS = self.__dict__.keys()

        # Default attribute dictionary

        self.dur    = self.attr['dur']      =  [0]
        self.root   = self.attr['root']     =  [0]
        self.degree = self.attr['degree']   =  [0]
        self.oct    = self.attr['oct']      =  [5]
        self.amp    = self.attr['amp']      =  [1]
        self.pan    = self.attr['pan']      =  [0]
        self.sus    = self.attr['sus']      =  [1]
        self.rate   = self.attr['rate']     =  [1]
        self.buf    = self.attr['buf']      =  [0]
        self.echo   = self.attr['echo']     =  [0]
        self.offset = self.attr['offset']   =  [0]
        self.freq   = [0]

    # --- Startup methods

    def reset(self):
        self.modf = dict([(key, [0]) for key in self.attr])
        self.modf['amp'] = 0.5
        return self    

    # --- Update methods

    def __call__(self):

        if self.stopping and self.metro.now() >= self.stop_point:
            self.kill()
            return

        if self.dur_updated(): self.event_n, self.event_index = self.count()

        # Get the current state

        self.get_event()

        # Get next occurence

        dur    = self.event[self._DUR]

        offset = self.event["offset"] - self.last_offset

        # Schedule the next event

        self.event_index = self.event_index + dur + offset
        
        self.metro.Schedule(self, self.event_index)

        # Store any offset

        self.last_offset = self.event["offset"]

        # Change internal marker

        self.event_n += 1 if not self.reversing else -1

        return

    def count(self):

        # Count the events that should have taken place between 0 and now()

        n = 0
        acc = 0
        dur = 0
        now = self.metro.now()

        while True:
            
            dur = modi(self.attr[self._DUR], n)

            if acc + dur > now:

                break

            else:
                
                acc += dur
                n += 1

        # Store duration times

        self.old_dur = self.attr['dur']

        # Returns value for self.event_n and self.event_index

        return n, acc

    def update(self):
        
        if self.isplaying is False:

            self.restart()

        return

    def dur_updated(self):
        return self.attr['dur'] != self.old_dur

    # --- Data methods

    def tupleN(self, exclude=None):
        """ Returns the length of the largest nested tuple in the attr dict """

        size = len(self.freq)
        
        for attr, value in self.event.items():
            if attr != exclude:
                try:
                    if len(value) > size:
                        size = len(value)
                except:
                    pass

        return size

    # --- Methods for preparing and sending OSC messages to SuperCollider

    def now(self, attr="degree", x=0):
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

        # If any values are time-dependant, get the now values

        try:

            attr_value = attr_value.now()

        except:

            pass

        try:

            modf_value = modf_value.now()

        except:

            pass

        # Combine attribute and modifier values

        try:

            # Amp is multiplied, not added

            if attr == "amp":

                value = attr_value * modf_value

            else:              
            
                value = attr_value + modf_value

        except:

            value = attr_value
        
        return value

    def get_event(self):
        """ Returns a dictionary of attr -> now values """

        self.event = {}
        
        for key in self.attr:

            self.event[key] = self.now(key)

        return self
            

    def osc_message(self, index=0, head=[]):
        """ Creates an OSC packet to play a SynthDef in SuperCollider """

        # Initial message plus custom head and echo variable

        message = [self.SynthDef, 0, 1, 1,
                   'echoON', int(self.event['echo'] > 0)] + head

        for key in self.attr:

            if key not in ('degree', 'oct', 'freq', 'dur', 'offset'):

                try:
                    
                    val = modi(self.event[key], index)

                    if key == "sus":

                        val = val * self.metro.beat_dur()

                    message += [key, float(val)]

                except:

                    pass

        return message

    def send(self):
        """ Sends the current event data to SuperCollder """

        # Get the current state in a dict
        
        for i in range(self.tupleN()):
            
            self.server.sendOSC( self.osc_message( i )  )

        return

    #: Methods for stop/starting players

    def kill(self):
        """ Removes this object from the Clock and resets itself"""
        self.isplaying = False
        self.isAlive = False
        self.event_n = 0
        self.offset = self.attr['offset'] = 0
        return
        
    def stop(self, N=0):
        
        """ Removes the player from the Tempo clock and changes its internal
            playing state to False in N bars time
            - When N is 0 it stops immediately"""

        self.stopping = True        
        self.stop_point = self.metro.beat

        if N > 0:

            self.stop_point += self.metro.NextBar() + ((N-1) * self.metro.Bar())

        return self

    def pause(self):

        self.isplaying = False

        return self

    def play(self):

        self.isplaying = True
        self.stopping = False
        self.isAlive = True

        self.__call__()

        return self

    def restart(self):

        self.isAlive = True
        self.stopping = False

        return self
        

    """
        Feeder Methods
        --------------

        These methods are used in conjunction with Patterns.Feeders functions.
        They change the state of the Player Object and return the object.

        See 'Player.Feeders' for more info on how to use

    """

    def lshift(self, n=1):
        self.event_n -= (n+1)
        return self

    def rshift(self, n=1):
        self.event_n += n
        return self

    def reverse(self):
        """ Sets flag to reverse streams """
        self.reversing = not self.reversing
        return self

    """

        Feeding Methods
        ---------------

        These methods will execute a Patterns.Feeders function (which use
        Player feeder methods) at points in time; regular or otherwise.

    """

    def every(self, n, cmd, *args):

        # Creates an expression unique to this object and function
        e = "'{0}'=='{0}' and '{1}'=='{1}'".format(cmd.__name__, id(self))

        if e not in self.when_statements:

            self.when_statements.append(e)

            self.metro.When(e, lambda: cmd(self), n, nextBar=True)

        else:

            self.metro.when_statements[e].step = n 

        return self

    """

        Modifier Methods
        ----------------

        Other modifiers for affecting the playback of Players

    """

    def offbeat(self, dur=0.5):
        """ Off sets the next event occurence """

        self.offset = self.attr['offset'] = dur

        return self

    def strum(self, dur=0.025):
        """ Adds a delay to a Synth Envelope """
        x = self.tupleN()
        if x > 1:
            self.delay = asStream([tuple(a * dur for a in range(x))])
        else:
            self.delay = asStream(dur)
        return self


    """

        Python's Magic Methods
        ----------------------

        Standard object operation methods

    """

    def __name__(self):
        for name, var in globals().items():
            if self == var: return name

    def __repr__(self):
        return "<Player ('%s')>" % self.SynthDef

    def __str__(self):
        return self.SynthDef

    def __setattr__(self, name, value):
        if self._INIT:
            if name not in self._VARS:
                value = asStream(value)
                self.attr[name] = value
        self.__dict__[name] = value

##################### SYNTH PLAYERS #####################

class SYNTH_PLAYER(PLAYER):

    _TYPE = _SYNTH_TYPE

    def __init__(self, SynthDef, degree=[0], **kwargs):

        # Inherit key methods

        PLAYER.__init__(self, SynthDef)

        # Update self with kwargs
        
        self.attr.update(kwargs)
        self.reset()

    def update(self, SynthDef, degree=[0], **kwargs):
        """ Updates the values of this Player """

        PLAYER.update(self)

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

            now[attr] = self.event[attr]

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

    def __call__(self):
        """ Calls the parent class update state then calculates frequency """
        PLAYER.__call__(self)
        self.freq = self.calculate_freq()
        self.send()

    def osc_message(self, index=0, head=[]):
        """ Attaches the frequency to the osc message """
        msg_head = ['freq', modi(self.freq, index)]
        return PLAYER.osc_message(self, index, msg_head)

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

    # Methods affecting other players - every n times, do a random thing?

    def stutter(self, n=2):
        """ repeats each value in each stream n times """

        # if n is a list, stutter each degree[i] by n[i] times

        self.degree = PStutter(self.degree, n)

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
        if isinstance(other, PLAYER):
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

BufferManager = Buffers.BufferManager().from_file()

class SAMPLE_PLAYER(PLAYER):

    _TYPE = _SAMPLES_TYPE
    _DUR  = 'dur_val'
    
    SPECIAL_CHARS = " []()"
    REST = SPECIAL_CHARS[0]

    def __init__(self, pat=' ', speed=[1], **kwargs):

        PLAYER.__init__(self, "sample_player")

        # Degree is the string of characters
        self.degree  = pat
        self.old_degree = ""

        # Real value of each sample duration
        self.dur_val = self.attr['dur_val'] = self.old_dur_val = None

        # Set samples a little louder
        self.amp = self.attr['amp'] = 1

        self.attr.update(kwargs)
        self.reset()
        
    def update(self, degree=" ", **kwargs):
        """ Updates the values of this Player """

        PLAYER.update(self)

        setattr(self, "degree", str(degree).replace("."," ") if len(degree) > 0 else " ")

        self.pat_to_buf()

        for name, value in kwargs.items():
            setattr(self, name, value)

        return self

    def __call__(self):
        """ String -> buffer numbers before clock update """
        PLAYER.__call__(self)
        self.old_dur_val = self.dur_val
        self.send()

    def dur_updated(self):
        return self.attr['dur'] != self.old_dur or self.attr['dur_val'] != self.old_dur_val

    def count(self):
        self.pat_to_buf()
        return PLAYER.count(self)        

    def pat_to_buf(self):
        """ Calculates the durations and buffer numbers based on the characters in the degree attribute """
        rhythm = PDur(self.degree, self.dur)

        self.attr['dur_val'] = self.dur_val = rhythm
 
        self.attr['buf'] = self.buf = [BufferManager.symbols.get(char, 0) for char in rhythm.chars]

        return

    def tupleN(self):
        """ Forces the tupleN method to skip out the degree attr when calculating the largest tuple """
        return PLAYER.tupleN(self, exclude='degree')

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

class Group:

    def __init__(self, *args):

        self.players = args

    def __len__(self):
        return len(self.players)

    def __setattr__(self, name, value):
        try:
            for i, p in enumerate(self.players):
                try:
                    setattr(p, name, value)
                except:
                    print "AttributeError: '%s' object has no attribute '%s'" % (str(p), name)
        except:
            self.__dict__[name] = value 
        return self        

    def __getattr__(self, name):
        """ Returns a Pattern object containing the desired attribute for each player in the group  """
        return P([player.__dict__[name] for player in self.players])

    def call(self, method, args):
        for p in self.players:
            p.__dict__[method].__call__(*args)

    def stop(self, n=0):
        for item in self.players:
            item.stop(n)
        return self

    def play(self):
        for item in self.players:
            item.play()
        return self

group = Group
