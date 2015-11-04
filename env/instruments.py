from OSC import OSCClient, OSCMessage, OSCBundle
from time import sleep, time
import Scale
import threading
import foxdot

# Functions for converting to frequency etc

def miditofreq(midinote):
    return 440 * (2 ** ((midinote - 69.0)/12.0))

def midi(scale, octave, degree, root=0, stepsPerOctave=12):

    lo = int(degree)
    hi = lo + 1

    octave = octave + (lo / len(scale))

    chroma = range(stepsPerOctave)

    scale_val = (scale[hi % len(scale)] - scale[lo % len(scale)]) * ((degree-lo)) + scale[lo % len(scale)]

    return scale_val + (octave * len(chroma)) + chroma[ root % len(chroma) ]


def Chord(stream, structure=[0,2,4]):

    new = []

    for item in stream:

        new.append([item + s for s in structure])

    return new
        

def Place(stream):
    """ nested streams are stretched
        e.g. [[1,0],0,1,0] would be returned as [1,0,1,0,0,0,1,0] """

    # If no nested values, return original stream

    try:

        largest_sub = max([len(a) for a in stream if type(a) == list])

    except:

        return stream

    new_stream = []

    for i in range( largest_sub ):

        for j in range(len(stream)):

            item = stream[j]

            if type(item) == list:

                item = item[i % len(item)]

            new_stream.append(item)
    
    return new_stream

def stutter_stream(stream, n):

    if type(n) == int:

        n = [n for i in stream]

    new_stream = []

    for i, item in enumerate(stream):

        for j in range(n[i]):

            new_stream.append( item )

    return new_stream    


# Converts data to list format

def asStream(data, n=" "):

    stream = None
    
    if   type(data) == list:
        stream = data
    elif type(data) == tuple:
        stream = list(data)
    elif type(data) == str:
        stream = list(data)
    else:
        try:
            if data.__type__ == "scale":
                stream = data
            else:
                stream = [data]
        except:
            stream = [data]

    return stream

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
        self.attr = {}
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

        # Add to aggregate counter for when events go past the clock scope

        if self.metro.beat == len(self.metro):

            self.event_agg += self.event_n

        # Execute any code in the mod_code list on desired beat

        for code in self.mod_code:
            
            foxdot.execute(code)

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

    def update_clock(self):

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

        # Aggregate event counter will be affected, so reset

        self.event_agg = 0

        return

    def update_dict(self):
        
        self.attr = {
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
                    }

    def now(self, attr, x=0):

        # Get which instrument is leading

        if self.following and attr is 'degree':

            attr_value = self.following.now('degree')

            modifier_event_n = self.event_n

        else:

            # Get the attr value + modifider value

            modifier_event_n = self.event_n

            attr_value = self.attr[attr][(self.event_n + x) % len(self.attr[attr])]

        modf_value = self.modf[attr][(modifier_event_n + x) % len(self.modf[attr])]

        try:

            if attr is "amp":

                value = attr_value * modf_value

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

        if type(data) == int or type(data) == float:

            data = [data]

        # Add to modifier

        self.modf['degree'] = data
        
        return self


    def __sub__(self, data):

        if type(data) == int or type(data) == float:

            data = [data]

        data = [d * -1 for d in data]

         # Add to modifier

        self.modf['degree'] = data

        return self

    def __mul__(self, data):

        """ Multiplying an instrument player multiplies each amp value by
            the input, or circularly if the input is a list. The input is
            stored here and calculated at the update stage """

        if type(data) in (int, float):

            data = [data]

        self.modf['amp'] = data

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

        self.degree = stutter_stream(self.degree, n)

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

    def osc_message(self, freq):

        message = [self.name, 0, 1, 1, 'freq', freq]

        for key in self.attr:

            if key not in ('freq', 'degree'):

                val = self.now(key)

                if key == "sus":

                    val = val * self.metro.beat_dur()

                message += [key, val]

        return message

    def send(self):
        """ Sends the current event data to SuperCollder """

        # Create OSC Message

        for f in self.freq:

            self.server.play_note( self.osc_message(f) )

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


class samples_:

    # Table of characters to buffers

    symbols = { 'x' : 1,    # Bass drum
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
        self.dur    = kwargs.get("dur",   [0.5])
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

        self.pat_to_buf()

        # Add to aggregate counter for when events go past the clock scope

        if self.metro.beat % len(self.metro) == 0:

            self.event_agg += self.event_n

        # Execute any code in the mod_code list on desired beat

        for when, code in self.mod_code:

            if self.metro.beat % (self.metro.beatsPerBar() * self.metro.steps) == (when - 1) * self.metro.steps:

                foxdot.execute(code)

        # Update dictionary to contain only streams

        self.update_dict()

        # If duration values changes, update the metronome

        if self.attr['dur'] != self.old_dur:

            self.update_clock()

            self.old_dur = self.attr['dur']

        return

    def update_clock(self):

        # Initial step, delete from the clock

        for step in self.metro:

            if self in step:

                step.remove(self)
                
        # Re-add to the clock with any updated values

        n = 0

        while n < len(self.metro):

            for dur in self.attr['dur']:

                self.metro.add2q(self, n)

                i = int(dur * self.metro.steps)                

                n += i

        # Aggregate event counter will be affected, so reset

        self.event_agg = 0

        return

    def update_dict(self):
        
        self.attr = {
                      "dur"     :   asStream(self.dur),
                      "amp"     :   asStream(self.amp),
                      "pan"     :   asStream(self.pan),
                      "rate"    :   asStream(self.rate),
                      "buf"     :   asStream(self.buf),
                      "verb"    :   asStream(self.verb),
                      "dist"    :   asStream(self.dist)
                    }

    def now(self, attr, x=0):

        # Get the attr value + modifider value

        modifier_event_n = self.event_n

        attr_value = self.attr[attr][(self.event_n + x) % len(self.attr[attr])]

        modf_value = self.modf[attr][(modifier_event_n + x) % len(self.modf[attr])]

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
        size_sus  = len(self.attr['sus'])
        size_data = len(data)

        size_max = max( size_dur , size_sus, size_data)

        self.dur = [ 0 for x in range(size_max) ]
        self.sus = [ 0 for x in range(size_max) ]

        for i in range( size_max ):

            self.dur[i] = self.attr['dur'][i % size_dur] / (1.0 / data[i % size_data])
            self.sus[i] = self.attr['sus'][i % size_sus] / (1.0 / data[i % size_data])

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

    def pat_to_buf2(self):

        self.buf = [self.symbols[char] for char in self.pat]

        return self
                
    def pat_to_buf(self):
        """ Converts s (a string) to a basic drum pattern.
            Items in a [] half half duration
            Items in a () are laced
        """

        self.dur = [max(self.dur) for char in self.pat]

        self.buf = [0 for char in self.pat]

        this_dur = 0

        # Go through pattern

        i = 0

        in_sq = False
        in_br = False
        in_wi = False

        for char in self.pat:

            if char in self.symbols.keys():

                if in_br:

                    self.buf[i].append( self.symbols[char] )
                    self.dur[i].append( this_dur )

                else:

                    self.buf[i] = self.symbols[char]

            # When we reach a [ divide duration by 2

            if   char == '[':

                in_sq = True

            elif char == ']':

                in_sq = False

            elif in_sq:

                if in_br:

                    self.dur[i].append(this_dur / 2.0)

                else:

                    self.dur[i] = self.dur[i] / 2.0

            elif char == '(':

                in_br = True

                this_dur = self.dur[i]

                self.buf[i] = []
                self.dur[i] = []

            elif char == ')':

                in_br = False

            # When we reach a ( don't increase i until )

            if not in_br and char not in "[]":

                i += 1

        # Adjust for extra chars

##        print self.buf[:i]
##        print Place(self.buf[:i])
##
##        print self.dur[:i]
##        print Place(self.dur[:i])

        self.buf = Place(self.buf[:i])
        self.dur = Place(self.dur[:i])

        return

    def stutter(self, n=4):
        
        """ repeats each value in each stream n times """

        self.pat = stutter_stream(self.pat, n)

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
