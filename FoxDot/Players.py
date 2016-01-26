"""
    Copyright Ryan Kirkbride 2015

    This module contains the objects for Instrument Players (those that send musical
    information to SuperCollider) and Sample Players (those that send buffer IDs to
    playback specific samples located in the Samples directory).

"""

from OSC import OSCClient, OSCMessage, OSCBundle
from Patterns import *

import Scale
import Code

# Functions for converting to frequency etc

def modi(array, i):
    """ Returns the modular index i.e. modi([0,1,2],4) will return 1 """
    try:
        return array[i % len(array)]
    except:
        return array
    

def miditofreq(midinote):
    """ Converts a midi number to frequency """
    return 440 * (2 ** ((midinote - 69.0)/12.0))

def midi(scale, octave, degree, root=0, stepsPerOctave=12):

    lo = int(degree)
    hi = lo + 1

    octave = octave + (lo / len(scale))

    chroma = range(stepsPerOctave)

    scale_val = (scale[hi % len(scale)] - scale[lo % len(scale)]) * ((degree-lo)) + scale[lo % len(scale)]

    return scale_val + (octave * len(chroma)) + chroma[ root % len(chroma) ]

def circular_add(a, b):
    """ Adding contents of b to a """
    if len(b) > len(a):
        tmp = b
        b = a
        a =tmp
        
    tmp = []
    
    for i in range(len(a)):

        tmp.append( a[i] + b[i % len(b)] )

    return tmp


###### Object used to perform basic methods on a multiple of players

class group:

    def __init__(self, *args):

        self.players = args

    def __len__(self):

        return len(self.players)

    def stop(self, n=0):

        for item in self.players:

            item.stop(n)

    def play(self):

        for item in self.players:

            item.play()

Group = group

###### Object for creating instruments

class new_:

    # Could create class variable that are shared by all instances?

    def __init__(self, var_name, name, degree=[0], **kwargs):

        self.name = name.lower()
        self.__name__ = var_name

        # Get metronome clock

        self.metro      = kwargs.get("metro", None)
        self.quantise   = kwargs.get("quantise", False)

        self.stopping = False
        self.stop_point = 0

        # Get server manager

        self.server = kwargs.get("server", None)

        # Points to a player to follow notes

        self.following = None

        # Define any variables that are used in the OSC message (make sure they are in the attr dict)

        self.dur    = kwargs.get("dur",     [1])
        self.scale  = kwargs.get("scale",   Scale.major)
        self.root   = kwargs.get("root",    [0])
        self.degree = kwargs.get("degree",  degree)
        self.oct    = kwargs.get("oct",     [5])
        self.amp    = kwargs.get("amp",     [0.5])
        self.pan    = kwargs.get("pan",     [0])
        self.sus    = kwargs.get("sus",     self.dur)
        self.rate   = kwargs.get("rate",    [1])
        self.pos    = kwargs.get("pos",     [0])
        self.buf    = kwargs.get("buf",     [0])

        # Modifiers

        self.mod_degree = [0]
        self.mod_code = []
        self.reversing = False

        # Sets the clock off a beat amount

        self.off = 0
        self.old_off = 0
        
        # Is calculated at each step
        self.freq   = [0]

        # Used to create glissandi on "slide"
        self.glissandi = bool(kwargs.get("glissandi", False))
        self.freq1  = [0]

        # Dictionary to read now() values from

        self.attr = kwargs

        for key in ['metro', 'server', 'quantise', 'glissandi']:
            if key in self.attr:
                del self.attr[key]
                
        self.update_dict()

        # Modifier dict
        self.modf = {}
        self.reset() # This method is used to 'reset' the modifiers

        # In case events go on past the scope of the clock, keep an aggregate that get's reset on clock updates

        self.event_agg = 0
        self.event_n   = 0
        self.event     = []

        # Used for checking clock updates
        
        self.old_dur = None
        self.isplaying = False

        self.metro.playing.append(self)

        self.update_clock()

        # reset beat counter

        # self.event_n = self.metro.beat % len(self.metro)

        #if self.metro:
            
        #    self.update(isEvent=False)

        #    if self.quantise:

        #        self.metro.playing.append(self)

        #    else:

        #        self.play()

    def __str__(self):

        return self.name

    def update2(self, isEvent=True):

        # Kill the player if stopping
        
        if self.stopping and self.metro.beat >= self.stop_point:

            self.kill()

        count = 0

        for step in self.metro.queue[:self.metro.now()]:

            if self in step:

                count += 1

        self.event_n = count

        # If the durations have been changed, re-calculate where it is in the passage

        # This player's event index is the number of occurences in the clock plus the number of occurences in previous clock loops

        # Add to aggregate counter for when events go past the clock scope

        if self.metro.beat == len(self.metro):

            self.event_agg += self.event_n

        # Execute any code in the mod_code list on desired beat

        for code in self.mod_code:
            
            Code.execute(code, verbose=False)

        # Check if the player is following another

        if self.following:

            self.degree = asStream( self.following.now('degree') )

        # Calculate frequency

        self.freq = [ miditofreq( midi( self.scale, self.now('oct'), DEGREE, self.now('root') ) ) for DEGREE in asStream(self.now('degree')) ]

        if self.glissandi:

            self.freq1.append(self.freq[-1])

        # Update dictionary to contain only streams

        self.update_dict()

         # If duration values changes, update the metronome

        if self.attr['dur'] != self.old_dur or self.off != self.old_off:

            self.update_clock()

            self.old_dur = self.attr['dur']
            self.old_off = self.off

        return

    def update(self, isEvent=True):

        # Kill the player if stopping
        
        if self.stopping and self.metro.beat >= self.stop_point:

            self.kill()

        if self.dur_updated():

            self.update_clock()

        else:

            self.event_n += int(isEvent)

        # Add to aggregate counter for when events go past the clock scope

        #if self.metro.beat == len(self.metro):

        #    self.event_agg += self.event_n

        # Execute any code in the mod_code list on desired beat

        for code in self.mod_code:
            
            Code.execute(code, verbose=False)

        # Check if the player is following another

        if self.following:

            self.degree = asStream( self.following.now('degree') )

        # Calculate frequency

        #self.freq = [ miditofreq( midi( self.scale, self.now('oct'), DEGREE, self.now('root') ) ) for DEGREE in asStream(self.now('degree')) ]

        # Find which has the greater length tuples in

        now_degree, now_oct = [asStream(self.now(attr)) for attr in ['degree', 'oct']]

        size = max( len(now_degree), len(now_oct) ) 

        self.freq = []

        for i in range(size):

            midinum = midi( self.scale, modi(now_oct, i), modi(now_degree, i) , self.now('root') )

            self.freq.append( miditofreq(midinum) )
            

        if self.glissandi:

            self.freq1.append(self.freq[-1])

        # Update dictionary to contain only streams

        self.update_dict()

        return

    def dur_updated(self):

        return self.attr['dur'] != self.old_dur or self.off != self.old_off 

    def update_clock2(self):

        # Could be done in 1 loop

        # Initial step, delete from the clock

        for step in self.metro:

            if self in step:

                step.remove(self)
                
        # Re-add to the clock with any updated values

        n = int(self.off * self.metro.steps)

        while n < len(self.metro):

            for dur in self.attr['dur']:

                self.metro.add2q(self, n)

                i = int(dur * self.metro.steps)

                n += i

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

                # Work out duration of the 

                #dur = self.attr['dur'][count % len(self.attr['dur'])]

                dur = modi(self.attr['dur'], count)

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

          #self.event_agg = 0

        self.old_dur = self.attr['dur']
        self.old_off = self.off

        return

    def update_dict(self):

        # Update the standard arguments
        
        self.attr.update( {
                              "scale"   :   asStream(self.scale),
                              "root"    :   asStream(self.root),
                              "degree"  :   asStream(self.degree),
                              "oct"     :   asStream(self.oct),
                              "sus"     :   asStream(self.sus),
                              "dur"     :   asStream(self.dur),
                              "amp"     :   asStream(self.amp),
                              "freq"    :   asStream(self.freq),
                              "freq1"   :   asStream(self.freq1),
                              "pan"     :   asStream(self.pan),
                              "rate"    :   asStream(self.rate),
                              "buf"     :   asStream(self.buf),
                              "pos"     :   asStream(self.pos)
                        } )

    def now(self, attr, x=0):

        # Get which instrument is leading

        if self.following and attr is 'degree':

            attr_value = self.following.now('degree')

            modifier_event_n = self.event_n

        else:

            # Get the attr value + modifider value

            modifier_event_n = self.event_n

            attr_value = modi(self.attr[attr], self.event_n + x)

        modf_value = modi(self.modf[attr], modifier_event_n + x)

        # Make sure values are numbers

        if attr is not "root":

            try:

                attr_value = float(attr_value)

            except:

                attr_value = tuple(float(v) for v in attr_value)

            try:

                modf_value = float(modf_value)

            except:

                modf_value = tuple(float(v) for v in modf_value)

        # Combine the attribute "real" values with the modifiers

        try:

            if attr is "amp":

                value = attr_value * modf_value

            elif (type(attr_value) == type(modf_value) == tuple):

                raise

            else:

                value = attr_value + modf_value

        except:

            # Both "chords" must have the same size or not used

            if type(attr_value) in (list, tuple) and type(modf_value) in (list, tuple):

                value = []

                for i, v in enumerate(attr_value):

                    value += [v + modf_value[i]]

            # Just original is chords

            elif type(attr_value) in (list, tuple) and type(modf_value) not in (list, tuple):

                value = [v + modf_value for v in attr_value]

            # Just modifier is chords

            elif type(attr_value) not in (list, tuple) and type(modf_value) in (list, tuple):

                value = [m + attr_value for m in modf_value]

            # Neither are chords

            else:

                value = attr_value
        
        return value

    def add(self, degree):
        """ Adds another copy of the event to the message with different degrees """

        self.event.append(degree)

        return self

    def pop(self):

        self.event = self.event[:-1]

        return self

    def reset(self):

        self.modf = dict([(key, [0]) for key in self.attr])

        self.modf['amp'] = [1]

        self.reset_code()

        return self

    def reset_code(self):

        self.mod_code = []

        return self

    def __add__(self, data):

        """ Change the degree modifier stream """

        self.modf['degree'] = asStream(data)
        
        return self


    def __sub__(self, data):

        # Set a state to add / sub? TODO

        if type(data) == int or type(data) == float:

            data = [data]

        data = [d * -1 for d in data]

         # Add to modifier

        self.modf['degree'] = asStream(data)

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

    def follow(self, lead):
        """ Takes a now object and then follows the notes """

        self.following = lead

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

    def every(self, n, code):
        """ Every n beats, execute code """

        # Check code?

        self.when("self.event_n %% %d == 0" % n, code)

        return self

    def when(self, statement, action):
        """ If statement is true, do the action """

        # Check syntax?

        if statement.count("=") == 1:

            statement.replace("=","==")

        if type(action) != list:

            action = [action]

        statement = statement.replace("self", self.__name__)

        s = "if %s:\n" % statement

        for code in action:

            s += "\t%s\n" % code.replace("self", self.__name__)

        self.mod_code.append(s)

        return self

    def offbeat(self, beat_len=0.5):
        """ Adds a 0 amplitude note to the start of the player"""

        self.off = beat_len

        return self    

    def reverse(self):
        """ Sets flag to reverse streams """

        self.dur.reverse()
        self.root.reverse()
        self.oct.reverse()
        self.amp.reverse()
        self.pan.reverse()
        self.sus.reverse()

        self.degree.reverse()

    # Methods affecting other players

    def bother(self, other):

        return self

    def stutter(self, n=4):
        """ repeats each value in each stream n times """

        # if n is a list, stutter each degree[i] by n[i] times

        self.degree = Stutter(self.degree, n)

        return self

    def kill(self):

        self.isplaying = False
        self.event_n = 0
        self.metro.playing.remove(self)

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

    def osc_message(self, index):

        message = [self.name, 0, 1, 1, 'freq', modi(self.freq, index)]

        for key in self.attr:

            if key not in ('freq', 'degree'):

                val = modi(self.now(key), index)

                if key == "sus":

                    val = val * self.metro.beat_dur()

                message += [key, val]

        return message

    def send(self):
        """ Sends the current event data to SuperCollder """

        # 1. Find out the largest tuple in the kwargs and its length

        size = len(self.freq)

        for stream in self.attr.values():

            for value in stream:

                try:

                    if len(value) > size:

                        size = len(value)

                except:

                    pass

        # Create OSC Message

        #for f in self.freq:
        
        for i in range(size):

            self.server.play_note( self.osc_message( i )  )       

        return

    def play(self):

        if self not in self.metro.playing:

            self.metro.playing.append(self)

        self.isplaying = True

        # Quantise

        self.event_n = self.metro.beat % len(self.metro) - int(self.quantise)

        self.stopping = False

        return self

    def start(self):

        self.play()

        return self


# ---------------------------------------------- #
# Class for for reading samples from buffers     # s = samples_("x-*-", metro=clock_, server=server_, quant=False)
# ---------------------------------------------- #

# Table of characters to buffers

#f = open("../samples/.symbols")


_symbols =  {   'x' : 1,    # Bass drum
                'X' : 2,    # Bass drum 2
                'o' : 3,    # Snare drum
                'O' : 4,    # Snare drum 2
                '*' : 5,    # Clap
                '-' : 6,    # Hi Hat Closed
                '=' : 7,    # Hi Hat Open
                'T' : 8,    # Cowbell
                '+' : 9,    # Cross stick
                'H' : 10,   # Noise burst
                'h' : 10,   # Noise burst
                'v' : 11,   # Kick drum
                'V' : 12,   # Kick drum 2
                's' : 13,   # Shaker
                'S' : 13,   # Shaker (it would be nice for a shaker 2)
                '~' : 14,   # Ride cymbal
                ':' : 15,   # Clicks
                '^' : 16,   # Tom tom
                '#' : 17,   # Crash
                'Y' : 18,   # Swoop
             }


class samples_:



    def __init__(self, pat=' ', speed=[1], **kwargs):

        self.name = "sample_player"

        # Get metronome clock

        self.metro      = kwargs.get("metro", None)
        self.quantise   = kwargs.get("quantise", False)
        self.stopping   = False
        self.stop_point = 0

        # Get server manager

        self.server = kwargs.get("server", None)

        # Points to a player to follow notes

        self.following = None

        # Define any variables that are used in the OSC message (make sure they are in the attr dict)

        self.pat    = pat
        self.old_pat = ""
        
        self.dur    = kwargs.get("dur",   [0.5])
        self.new    = self.dur # "new" value after brackets
        self.amp    = kwargs.get("amp",     [1])
        self.pan    = kwargs.get("pan",     [0])
        self.rate   = kwargs.get("rate",    [1])
        self.verb   = kwargs.get("verb",  [0.2])
        self.dist   = kwargs.get("dist",    [0])

        # Map pattern to buffer numbers
        
        self.buf    = kwargs.get("buf", [0])

        # Modifiers
        
        self.mod_code = []
        self.reversing = False

        # Dictionary to read now() values from
        self.attr = {}
        self.update_dict()

        # Update the buffer numberss

        self.pat_to_buf()

        # Modifier dict
        self.modf = {}
        self.reset() # This method is used to 'reset' the modifiers

        # In case events go on past the scope of the clock, keep an aggregate that get's reset on clock updates

        self.event_agg = 0
        self.event_n = 0
        self.event   = []

        # Used for checking clock updates
        
        self.old_dur = None
        self.old_new = None
        self.isplaying = False

        # reset beat counter

        # self.event_n = self.metro.beat % len(self.metro)

        if self.metro:
            
            self.update(isEvent=False)

            if self.quantise:

                self.metro.playing.append(self)

            else:

                self.play()

    def __str__(self):

        return self.name

    def update(self, isEvent=True):

        # Kill the player if stopping

        if self.stopping:

            if self.metro.beat >= self.stop_point:

                self.kill()
                
        # Find out the number of events in the clock before the current beat pointer

        count = 0

        for step in self.metro.queue[:self.metro.now()]:

            if self in step:

                count += 1

        # This player's event index is the number of occurences in the clock plus the number of occurences in previous clock loops

        self.event_n = count + self.event_agg

        # If the pattern has changed, update values

        if self.pat != self.old_pat or self.dur != self.old_dur:

            self.old_pat = self.pat
            self.old_dur = self.dur

            self.pat_to_buf()

        # Add to aggregate counter for when events go past the clock scope

        if self.metro.beat % len(self.metro) == 0:

            self.event_agg += self.event_n

        # Execute any code in the mod_code list on desired beat

        for when, code in self.mod_code:

            if self.metro.beat % (self.metro.beatsPerBar() * self.metro.steps) == (when - 1) * self.metro.steps:

                Code.execute(code)

        # Update dictionary to contain only streams

        self.update_dict()

        # If duration values changes, update the metronome

        if self.attr['new'] != self.old_new:

            self.update_clock()

            self.old_new = self.attr['new']

        return

    def update_clock(self):

        # Initial step, delete from the clock

        for step in self.metro:

            if self in step:

                step.remove(self)
                
        # Re-add to the clock with any updated values

        n = 0

        while n < len(self.metro):

            for dur in self.attr['new']:

                self.metro.add2q(self, n)

                i = int(float(dur) * self.metro.steps)                

                n += i

        # Aggregate event counter will be affected, so reset

        self.event_agg = 0

        return

    def update_dict(self):
        
        self.attr.update( {
                      "dur"     :   asStream(self.dur),
                      "new"     :   asStream(self.new),
                      "amp"     :   asStream(self.amp),
                      "pan"     :   asStream(self.pan),
                      "rate"    :   asStream(self.rate),
                      "buf"     :   asStream(self.buf),
                      "verb"    :   asStream(self.verb),
                      "dist"    :   asStream(self.dist)
                    } )

    def now(self, attr, x=0):

        # Get the attr value + modifider value

        modifier_event_n = self.event_n

        attr_value = float(self.attr[attr][(self.event_n + x) % len(self.attr[attr])])

        modf_value = float(self.modf[attr][(modifier_event_n + x) % len(self.modf[attr])])

        try:

            value = attr_value + modf_value

        except:

            value = attr_value
        
        return value

    def reset(self):

        self.modf = dict([(key, [0]) for key in self.attr])

        self.reset_code()

        return self

    def reset_code(self):

        self.mod_code = []

        return self

    def __add__(self, data):

        if type(data) == int:

            self.amp = [a + data for a in self.amp]

            return self

        if type(data) == str:

            self.pat += data

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

    def every(self, n, code):
        """ Every n beats, execute code """

        # Check code?

        if (n, code) not in self.mod_code:

            self.mod_code.append( (n, code) )

        return self

    def reverse(self):
        """ Sets flag to reverse streams """

        self.dur.reverse()
        self.amp.reverse()
        self.pan.reverse()
        self.buf.reverse()

        self.pat = list(self.pat)
        self.pat.reverse()


        return self

    # Methods affecting other players

    def bother(self, other):

        return self


    # Drum methods

    def pat_to_buf3(self):

        self.buf = [self.symbols[char] for char in self.pat]

        return self
                
    def pat_to_buf(self):
        """ Converts s (a string) to a basic drum pattern.
            Items in a [] half half duration
            Items in a () are laced
        """

        if not len(self.pat) > 0:

            self.pat = " "

        self.new = asStream(self.dur)

        new_dur  = [modi(self.new, i) for i, char in enumerate(self.pat) if char not in "[](){}"]

        self.buf = [0 for char in self.pat if char not in "[](){}"]

        # Go through pattern

        i = 0

        this_dur = modi(self.new, i)

        in_sq = 0
        in_br = False
        in_wi = False

        for char in self.pat:

            # When we reach a [ divide duration by 2

            if char == '[':

                in_sq += 1

            elif char == ']':

                in_sq -= 1

            # When we reach a ( create a list to add entries to
            
            elif char == '(':

                in_br = True

                self.buf[i] = []
                new_dur[i] = []

            elif char == ')':

                in_br = False
                i = i+1

            # Add the buffer number -> is 0 if not in _symbols
            
            else:

                # Normal brackets indicate a group to be laced

                if in_br:

                    self.buf[i].append( _symbols.get(char, 0) )
                    new_dur[i].append( this_dur / (2.0**in_sq) )

                else:

                    self.buf[i] = _symbols.get(char, 0)
                    new_dur[i] = this_dur / (2.0**in_sq)

            # When we reach a ( don't increase i until )

            if not in_br and char not in "[]()":

                i += 1

                this_dur = modi(self.new, i)

        # Adjust for extra chars

        self.buf = Place(self.buf[:i])
        self.new = Place(new_dur[:i])

        return

    def stutter(self, n=4):
        
        """ repeats each value in each stream n times """

        self.pat = Stutter(self.pat, n)

        return self

    def kill(self):

        self.isplaying = False
        self.event_n = 0
        self.metro.playing.remove(self)

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

    def osc_message(self):

        message = [self.name, 0, 1, 1]

        for key in self.attr:

            message += [key, self.now(key)]

        return message

    def send(self):
        """ Sends the current event data to SuperCollder """

        # Create OSC Message

        # self.update()

        self.server.play_note( self.osc_message() )

        return

    def play(self):

        if self not in self.metro.playing:

            self.metro.playing.append(self)

        self.isplaying = True

        # Quantise

        self.event_n = self.metro.beat % len(self.metro) - int(self.quantise)

        self.stopping = False

        return self

    def start(self):

        self.play()

        return self
