"""
    Copyright Ryan Kirkbride 2015

    This module contains the objects for Instrument Players (those that send musical
    information to SuperCollider) and Sample Players (those that send buffer IDs to
    playback specific samples located in the Samples directory).

"""

from os.path import dirname
from random import shuffle
from copy import copy

from Settings import SamplePlayer
from Code import WarningMsg
from SCLang.SynthDef import SynthDefProxy
from Repeat import *
from Patterns import *
from Midi import *

from Bang import Bang

import Scale
import Buffers
import TimeVar

BufferManager = Buffers.BufferManager()

class Player(Repeatable):

    # These are the PlayerObject attributes NOT included in OSC messages
    VARS = []
    # This is an internal flag 
    INIT = False
    # Used for visual feedback
    bang_kwargs = {}

    keywords   = ('degree', 'oct', 'freq', 'dur', 'delay', 'blur', 'amplify', 'scale', 'bpm')
    Attributes = keywords + ('sus', 'bits', 'chop', 'rate', 'scrub', 'pan', 'echo', 'amp', 'fmod', 'buf', 'vib')
    
    metro = None
    server = None

    # Tkinter Window
    widget = None

    def __init__( self ):

        # Inherit

        Repeatable.__init__(self)
        
        self.synthdef = None
        self.id = None
        self.quantise = False
        self.stopping = False
        self.stop_point = 0
        self.following = None
        self.playstring = ""

        # Visual feedback information

        self.envelope    = None
        self.line_number = None
        self.whitespace  = None
        self.bang_kwargs = {}

        # Modifiers
        
        self.reversing = False
        self.degrading = False
        
        # Keeps track of which note to play etc

        self.event_index = 0
        self.event_n = 0
        self.notes_played = 0
        self.event = {}

        # Used for checking clock updates
        
        self.old_dur = None
        self.old_pattern_dur = None
        
        self.isplaying = False
        self.isAlive = True

        # These dicts contain the attribute and modifier values that are sent to SuperCollider

        self.attr  = {}
        self.modf  = {}

        # Keyword arguments that are used internally

        self.scale = None
        self.offset  = 0
        
        # List the internal variables we don't want to send to SuperCollider

        self.VARS = self.__dict__.keys()

        self.INIT = True

        self.reset()

        #### end of init

    """ The PlayerObject Method >> """

    def __rshift__(self, other):
        # Player Object Manipulation
        if isinstance(other, SynthDefProxy):
            self.update(other.name, other.degree, **other.kwargs)
            self + other.mod
            self.envelope = other.env
            for method, arguments in other.methods.items():
                args, kwargs = arguments
                getattr(self, method).__call__(*args, **kwargs)                
            return self
        raise TypeError("{} is an innapropriate argument type for PlayerObject".format(other))
        return self

    def __setattr__(self, name, value):
        if self.INIT:
            # Force the data into a TimeVar or Pattern if the attribute is used with SuperCollider
            if name not in self.VARS:
                value = asStream(value) if not isinstance(value, (PlayerKey, TimeVar.var)) else value
                self.attr[name] = value
                return
        self.__dict__[name] = value
        return

    # --- Startup methods

    def reset(self):

        # --- SuperCollider Keywords

        # Left-Right panning (-1,1)
        self.pan     = 0

        # Sustain and blur (aka legato)
        self.sus     = 1

        # Amplitude
        self.amp     = 1

        # Rate - varies between SynthDef
        self.rate    = 1
        
        # Audio sample buffer number
        self.buf     = 0

        # Echo amount
        self.echo    = 0

        self.fmod   =  0

        # --- FoxDot Keywords
        
        # Duration of notes
        self.dur     = 0.5 if self.synthdef is SamplePlayer else 1
        self.old_pattern_dur = self.old_dur = self.attr['dur']

        self.delay   = 0

        # Degree of scale / Characters of samples

        self.degree  = " " if self.synthdef is SamplePlayer else 0

        # Octave of the note
        self.oct     = 5

        # Amplitude mod
        self.amplify = 1
        
        # Legato
        self.blur    = 1
        
        # Tempo
        self.bpm     = None 

        # Frequency and modifier
        self.freq   =  0

        # Offbeat delay
        self.offset = 0
        
        self.modf = dict([(key, [0]) for key in self.attr])
        return self

    # --- Update methods

    def __call__(self):

        # If stopping, kill the event

        if self.stopping and self.metro.now() >= self.stop_point:
            self.kill()
            return

        # If the duration has changed, work out where the internal markers should be

        if self.dur_updated():

            self.event_n, self.event_index = self.count()

            self.old_dur = self.attr['dur']
        
        # Get the current state

        dur = 0

        while True:

            self.get_event()
            
            dur = float(self.event['dur'])

            if dur == 0:

                self.event_n += 1

            else:

                break

        # Play the note

        if self.metro.solo == self: # TODO this syntax is ambiguous

            self.freq = 0 if self.synthdef is SamplePlayer else self.calculate_freq()

            self.send()

        # If using custom bpm

        if self.event['bpm'] is not None:

            dur *= (float(self.metro.bpm) / float(self.event['bpm']))

        # Schedule the next event

        self.event_index = self.event_index + dur
        
        self.metro.schedule(self, self.event_index)

        # Change internal marker

        self.event_n += 1 if not self.reversing else -1
        self.notes_played += 1

        return

    def count(self, time=None):

        # Count the events that should have taken place between 0 and now()

        n = 0
        acc = 0
        dur = 0
        now = time if time is not None else self.metro.now()

        durations = self.rhythm()
        total_dur = sum(durations)

        if total_dur == 0:

            WarningMsg("Player object has a total duration of 0. Set to 1")
            
            self.dur = total_dur = durations = 1
    
        acc = now - (now % total_dur)
        n = int(len(durations) * (acc / total_dur))

        while True:
            
            dur = float(modi(durations, n))

            if acc + dur > now:

                break

            else:
                
                acc += dur
                n += 1

        # Store duration times

        self.old_dur = self.attr['dur']

        # Returns value for self.event_n and self.event_index

        self.notes_played = n

        return n, acc

    def update(self, synthdef, degree, **kwargs):

        # SynthDef name
        
        self.synthdef = synthdef

        if self.isplaying is False:

            self.reset()

        # If there is a designated solo player when updating, add this at next bar
        
        if self.metro.solo.active() and self.metro.solo != self:

            self.metro.schedule(lambda: self.metro.solo.add(self), self.metro.next_bar() - 0.001)

        # Update the attribute values

        special_cases = ["scale", "root", "dur"]

        # Set the degree

        if synthdef is SamplePlayer:

            self.playstring = degree

            setattr(self, "degree", degree if len(degree) > 0 else " ")

        elif degree is not None:

            self.playstring = str(degree)

            setattr(self, "degree", degree)

        # Set special case attributes

        self.scale = kwargs.get("scale", self.__class__.default_scale )
        self.root  = kwargs.get("root",  self.__class__.default_root )

        # If only duration is specified, set sustain to that value also

        if "dur" in kwargs:
            
            self.dur = Pattern([list(i) if isinstance(i, PGroup) else i for i in asStream(kwargs['dur'])])

            if "sus" not in kwargs:

                self.sus = self.attr['dur']

        if synthdef is SamplePlayer: pass

            # self.old_pattern_dur

            # self.old_dur = self.attr['dur']

        # Set any other attributes

        for name, value in kwargs.items():

            if name not in special_cases:

                setattr(self, name, value)

        # Calculate new position if not already playing

        if self.isplaying is False:

            # Add to clock        
            self.isplaying = True
            self.stopping = False
            
            self.event_index = self.metro.next_bar()
            self.event_n = 0

            self.event_n, _ = self.count(self.event_index)
            
            self.metro.schedule(self, self.event_index)

        return self

    def dur_updated(self):
        dur_updated = self.attr['dur'] != self.old_dur
        if self.synthdef == SamplePlayer:
            dur_updated = (self.pattern_rhythm_updated() or dur_updated)
        return dur_updated

    def step_duration(self):
        return 0.5 if self.synthdef is SamplePlayer else 1    

    def rhythm(self):
        # If a Pattern TimeVar
        if isinstance(self.attr['dur'], TimeVar.Pvar):
            r = asStream(self.attr['dur'].now().data)
            
        # If duration is a TimeVar
        elif isinstance(self.attr['dur'], TimeVar.var):
            r = asStream(self.attr['dur'].now())
            
        else:
            r = asStream(self.attr['dur']) 

        # TODO: Make sure degree is a string
        if self.synthdef is SamplePlayer:
            try:
                d = self.attr['degree'].now()
            except:
                d = self.attr['degree']
            r = r * [(char.dur if hasattr(char, "dur") else 1) for char in d.flat()]
        return r

    def pattern_rhythm_updated(self):
        r = self.rhythm()
        if self.old_pattern_dur != r:
            self.old_pattern_dur = r
            return True
        return False

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

    def calculate_freq(self):
        """ Uses the scale, octave, and degree to calculate the frequency values to send to SuperCollider """

        # If the scale is frequency only, just return the degree

        if self.scale == Scale.freq:
            
            try:

                return list(self.event['degree'])

            except:

                return [self.event['degree']]

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

            try:
                
                midinum = midi( self.scale, modi(now['oct'], i), modi(now['degree'], i) , self.now('root') )

            except:

                WarningMsg("Invalid degree / octave arguments for frequency calculation, reset to default")

                raise

            f.append( miditofreq(midinum) )
            
        return f

    def f(self, *data):

        """ adds value to frequency modifier """

        self.fmod = tuple(data)

        p = []
        for val in self.attr['fmod']:

            try:
                pan = tuple((item / ((len(val)-1) / 2.0))-1 for item in range(len(val)))
            except:
                pan = 0
            p.append(pan)

        self.pan = p

        return self

    # Methods affecting other players - every n times, do a random thing?

    def stutter(self, n=2):
        """ Plays the current note n-1 times over the current durations """
    
        if self.metro.solo == self and n >  0:
            
            size = self.largest_attribute()

            n = int(n)

            dur = float(self.event['dur']) / n

            for stutter in range(1, n):

                for i in range(size):

                    osc_msg = self.osc_message(i)

                    delay = modi(self.event['delay'], i)
                    amp   = modi(self.event['amp'], i)
                    buf   = modi(self.event['buf'], i)

                    # Any messages with zero amps or 0 buf are not sent

                    if (self.synthdef != SamplePlayer and amp > 0) or (self.synthdef == SamplePlayer and buf > 0 and amp > 0):

                        delay += (stutter * dur)

                        self.metro.schedule(self.send, self.event_index + delay)
                        self.metro.schedule(self.bang, self.metro.now() + delay)
                    
        return self

    # TODO
    def spin(self, amount=4):
        # Stutter but with pan all around
        return self

    # --- Misc. Standard Object methods

    def __int__(self):
        return int(self.now('degree'))

    def __float__(self):
        return float(self.now('degree'))

    def __add__(self, data):
        """ Change the degree modifier stream """
        self.modf['degree'] = asStream(data)
        return self

    def __sub__(self, data):
        """ Change the degree modifier stream """
        data = asStream(data)
        data = [d * -1 for d in data]
        self.modf['degree'] = data
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

    # --- Data methods

    def largest_attribute(self):
        """ Returns the length of the largest nested tuple in the attr dict """

        # exclude = 'degree' if self.synthdef is SamplePlayer else None
        exclude = None

        size = len(self.attr['freq'])

        for attr, value in self.event.items():
            if attr != exclude:
                try:
                    l = len(value)
                    if l > size:
                        size = l
                except:
                    pass

        return size

    # --- Methods for preparing and sending OSC messages to SuperCollider

    def now(self, attr="degree", x=0):
        """ Calculates the values for each attr to send to the server at the current clock time """

        modifier_event_n = self.event_n

        attr_value = self.attr[attr]

        attr_value = modi(asStream(attr_value), self.event_n + x)
        
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
            
            value = attr_value + modf_value

        except:

            value = attr_value
            
        return value

    def get_event(self):
        """ Returns a dictionary of attr -> now values """

        # Get the current event

        self.event = {}

        attributes = copy(self.attr)
        
        for key in attributes:

            # Eg. sp.sus returns the currently used value for sustain

            self.event[key] = self.now(key)

            #  Make sure the object's dict uses PlayerKey instances

            if key not in self.__dict__:

                self.__dict__[key] = PlayerKey(self.event[key])

            elif not isinstance(self.__dict__[key], PlayerKey):

                self.__dict__[key] = PlayerKey(self.event[key]) 

            else:

                self.__dict__[key].update(self.event[key])

        # Special case: sample player

        if self.synthdef is SamplePlayer:

            event_buf = list(range(len(self.event['degree'])))
            event_dur = self.event['dur']

            for i, bufchar in enumerate(self.event['degree']):

                char = BufferManager[bufchar]

                # Get the buffer number to play
                buf_mod_index = modi(self.event['buf'], i)

                event_buf[i] = char.bufnum(buf_mod_index)

                # Apply any duration ratio changes

                try:
                    
                    self.event['dur'] *= bufchar.dur

                except:

                    pass

            self.event['buf'] = P(event_buf)

        return self

    def osc_message(self, index=0):
        """ Creates an OSC packet to play a SynthDef in SuperCollider """

        freq = float(modi(self.attr['freq'], index))
        
        message = ['freq',  freq ]

        attributes = self.attr

        for key in attributes:

            if key not in self.keywords:

                try:
                    
                    val = modi(self.event[key], index)

                    # Special case modulation

                    if key == "sus":

                        val = val * self.metro.beat() * modi(self.event['blur'], index)

                    elif key == "echo":

                        val = val * self.metro.beat() * modi(self.event['blur'], index)

                        message += ['echoOn', int(val > 0)]

                    elif key == "amp":

                        val = val * modi(self.event['amplify'], index)

                    message += [key, float(val)]

                except:
                    
                    print("Error generating OSC message for '{}'. Problem with {}".format(self.synthdef, key))

        return message

    def send(self):
        """ Sends the current event data to SuperCollder """

        size = self.largest_attribute()
        banged = False
        sent_messages = []

        for i in range(size):

            osc_msg = self.osc_message(i)

            delay = modi(self.event['delay'], i)
            amp   = modi(self.event['amp'], i)
            buf   = modi(self.event['buf'], i)

            # Any messages with zero amps or 0 buf are not sent

            if (self.synthdef != SamplePlayer and amp > 0) or (self.synthdef == SamplePlayer and buf > 0 and amp > 0):

                if delay > 0:

                    self.metro.schedule(send_delay(self, osc_msg), self.event_index + delay)
                    self.metro.schedule(self.bang, self.metro.now() + delay)
                    
                else:

                    # Don't send duplicate messages

                    if osc_msg not in sent_messages:
                    
                        self.server.sendNote(str(self.synthdef), osc_msg)

                        sent_messages.append(osc_msg)

                    if not banged:

                        self.bang()

                        banged = True
        return

    #: Methods for stop/starting players

    def kill(self):
        """ Removes this object from the Clock and resets itself"""
        self.isplaying = False
        self.repeat_events = {}
        self.reset()
        return
        
    def stop(self, N=0):
        
        """ Removes the player from the Tempo clock and changes its internal
            playing state to False in N bars time
            - When N is 0 it stops immediately"""

        self.stopping = True        
        self.stop_point = self.metro.now()

        if N > 0:

            self.stop_point += self.metro.next_bar() + ((N-1) * self.metro.bar_length())

        else:

            self.kill()

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

    def follow(self, lead, follow=True):
        """ Takes a now object and then follows the notes """

        self.degree = lead.degree

        return self

    def solo(self, arg=True):

        if arg:
            
            self.metro.solo.set(self)

        else:

            self.metro.solo.reset()

        return self

    def num_key_references(self):
        """ Returns the number of 'references' for the
            attr which references the most other players """
        num = 0
        for attr in self.attr.values():
            if isinstance(attr, PlayerKey):
                if attr.num_ref > num:
                    num = attr.num_ref
        return num
        

    """
        State-Shift Methods
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
        if self.reversing:
            self.event_n -= 1
        else:
            self.event_n += 1
        return self

    def shuffle(self):
        """ Shuffles the degree of a player. If possible, do it visually """
        if self.synthdef == SamplePlayer:
            self._replace_string(PlayString(self.playstring).shuffle())
        else:
            self._replace_degree(self.attr['degree'].shuffle())
            # self.degree = self.attr['degree'].shuffle()
        return self

    def mirror(self):
        if self.synthdef == SamplePlayer:
            self._replace_string(PlayString(self.playstring).mirror())
        else:
            self._replace_degree(self.attr['degree'].mirror())
            #self.degree = self.attr['degree'].mirror()
        return self

    def rotate(self, n=1):
        if self.synthdef == SamplePlayer:
            self._replace_string(PlayString(self.playstring).rotate(n))
        else:
            self._replace_degree(self.attr['degree'].rotate(n))
            #self.degree = self.attr['degree'].rotate(n)
        return self

    def splice(self):
        # [0,1,2,3,4] -> [0,3,2,1,4] (rotate every other val)
        return self

    def _replace_string(self, new_string):
        # Update the GUI if possible
        if self.widget:
            # Replace old_string with new string
            self.widget.addTask(target=self.widget.replace, args=(self.line_number, self.playstring, new_string))
        self.playstring = new_string
        setattr(self, 'degree', new_string)
        return

    def _replace_degree(self, new_degree):
        # Update the GUI if possible
        if self.widget:
            # Replace old_string with new string
            self.widget.addTask(target=self.widget.replace_re, args=(self.line_number,), kwargs={'new':str(new_degree)})
        self.playstring = str(new_degree)
        setattr(self, 'degree', new_degree)
        return

    def multiply(self, n=2):
        self.attr['degree'] = self.attr['degree'] * n
        return self

    def degrade(self, amount=0.5):
        """ Sets the amp modifier to a random array of 0s and 1s
            amount=0.5 weights the array to equal numbers """
        if not self.degrading:
            self.amp = Pwrand([0,1],[1-amount, amount])
            self.degrading = True
        else:
            ones = int(self.amp.count(1) * amount)
            zero = self.amp.count(0)
            self.amp = Pshuf(Pstutter([1,0],[ones,zero]))
        return self            

    """

        Modifier Methods
        ----------------

        Other modifiers for affecting the playback of Players

    """

    def offbeat(self, dur=0.5):
        """ Off sets the next event occurence """

        self.attr['delay'] += (dur-self.offset)

        self.offset = dur

        return self

    def strum(self, dur=0.025):
        """ Adds a delay to a Synth Envelope """
        x = self.largest_attribute()
        if x > 1:
            self.delay = asStream([tuple(a * dur for a in range(x))])
        else:
            self.delay = asStream(dur)
        return self

    def __repr__(self):
        return "a '%s' Player Object" % self.synthdef

    def info(self):
        s = "Player Instance using '%s' \n\n" % self.synthdef
        s += "ATTRIBUTES\n"
        s += "----------\n\n"
        for attr, val in self.attr.items():
            s += "\t{}\t:{}\n".format(attr, val)
        return s

    def bang(self, **kwargs):
        """
        Triggered when sendNote is called. Responsible for any
        action to be triggered by a note being played. Default action
        is underline the player
        """
        if kwargs:

            self.bang_kwargs = kwargs

        elif self.bang_kwargs:

            bang = Bang(self, self.bang_kwargs)

        return self

####
class PlayerKey:
    def __init__(self, value=None, reference=None):
        self.value = asStream(value)
        self.index = 0
        if reference is None:
            self.other   = 0
            self.num_ref = 0
        else:
            self.other   = reference
            self.num_ref = reference.num_ref + 1
            print "num_ref", self.num_ref
    @staticmethod
    def calculate(x, y):
        return x
    def update(self, value):
        self.value = asStream(value)
        return
    def __add__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Add
        return new
    def __radd__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rAdd
        return new
    def __sub__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Sub
        return new
    def __rsub__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rSub
        return new
    def __mul__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Mul
        return new
    def __rmul__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rMul
        return new
    def __div__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Div
        return new
    def __rdiv__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rDiv
        return new
    def __mod__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Mod
        return new
    def __rmod__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rMod
        return new
    def __pow__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Pow
        return new
    def __rpow__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rPow
        return new
    def __xor__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Pow
        return new
    def __rxor__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rPow
        return new
    def __truediv__(self, other):
        new = PlayerKey(other, self)
        new.calculate = Div
        return new
    def __rtruediv__(self, other):
        new = PlayerKey(other, self)
        new.calculate = rDiv
        return new
    # Comparisons
    def __eq__(self, other):
        return self.now(step=0) == other
    def __ne__(self, other):
        return self.now(step=0) != other
    def __gt__(self, other):
        return self.now(step=0) > other
    def __lt__(self, other):
        return self.now(step=0) < other
    def __ge__(self, other):
        return self.now(step=0) >= other
    def __le__(self, other):
        return self.now(step=0) <= other

    # Values
    def __int__(self):
        return int(self.now())
    def __float__(self):
        return float(self.now())
    def __str__(self):
        return str(self.now())
    def __repr__(self):
        return repr(self.now())
    def __len__(self):
        return len(self.now())
    def now(self, step=1):
        if isinstance(self.other, self.__class__):
            other = self.other.now(step=0)
        else:
            other = self.other
        value = self.calculate(self.value[self.index], other)
        self.index += step
        return value


class send_delay:
    """ Holds the state of a player whose send has
        been scheduled in the future """
    def __init__(self, s, message):
        self.server = s.server
        self.synth = s.synthdef
        self.msg = message
    def __call__(self):
        self.server.sendNote(self.synth, self.msg)


###### GROUP OBJECT

class Group:

    def __init__(self, *args):

        self.players = args

    def __len__(self):
        return len(self.players)

    def __str__(self):
        return str(self.players)

    def __setattr__(self, name, value):
        try:
            for p in self.players:
                try:
                    setattr(p, name, value)
                except:
                    WarningMsg("'%s' object has no attribute '%s'" % (str(p), name))
        except:
            self.__dict__[name] = value 
        return self        

    def __getattr__(self, name):
        """ Returns a Pattern object containing the desired attribute for each player in the group  """
        if name == "players":
            return self.players
        attributes = GroupAttr()
        for player in self.players:
            if hasattr(player, name):
                attributes.append(getattr(player, name))
        return attributes

class GroupAttr(list):
    def __call__(self, *args, **kwargs):
        for p in self:
            if callable(p):
                p.__call__(*args, **kwargs)
        
