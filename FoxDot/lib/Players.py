"""
    Making music with FoxDot Players
    --------------------------------
    
    Players are what make FoxDot make music. They are similar in design to
    SuperCollider's `PDef` and `PBind` combo but with slicker syntax. FoxDot
    uses SuperCollider to *actually* make the sound and does so by triggering
    predefined `SynthDefs` - sort of like definitions of a digital instruments.
    To have a look at the list of `SynthDefs`, you can just `print` them to
    the console:

    ```python
    print SynthDefs
    ```

    Each one of these represents a `SynthDef` *object*. These objects are then
    given to Players to play - like giving an instrument to someone in your
    orchestra. To give someone the instrument, `pads`, you use a double arrow
    some code syntax like this:

    ```python
    p1 >> pads()
    ```

    `p1` is the name of a predefined player object. At startup, FoxDot reserves
    all one- and two-character variable names, such as `x`, `p1`, or `bd` for
    player objects but these can be repurposed if you like. If you want to use
    a variable name for a player object with more than two characters, you just
    instantiate a new `Player` object:

    ```python
    new_player = Player()

    new_player >> pads()
    ```

    Changing parameters
    -------------------

    By default, player objects play the first note of their default scale (more
    below) with a duration of 1 beat per note. To change the pitch just give the
    `SynthDef` a list of numbers.

    ```python
    p1 >> pads([0,7,6,4])
    ```    

    When you start FoxDot up, your clock is ticking at 120bpm and your player
    objects are all playing in the major scale. With 8 pitches in the major scale,
    the 0 refers to the first pitch and the 7 refers to the pitch one octave
    higher because Python, like most programming languages, uses zero-indexing.
    To change your scale you can specify a new scale as a keyword argument (see
    the documentation on `Scales` for more information on scales) or change the
    default scale for all player objects.

    ```python
    # Changing scale as a keyword argument
    p1 >> pads([0,7,6,4], scale=Scale.minor)

    # Changing the default scalew (the following are equivalent)
    Scale.default.set("minor")
    Scale.default.set(Scale.minor)
    Scale.default.set([0,2,3,5,7,8,10])

    # See a list of scales
    print Scale.names()

    # Change the tempo
    Clock.bpm = 144
    ```

    To change the rhythm of your player object, specify the durations using
    the `dur` keyword. Other keywords can be specified, such as `oct` for the
    octave and `sus` for the sustain, which is the same as the duration by
    default.

    ```python
    p1 >> pads([0,7,6,4], dur=[1,1/2,1/4,1/4], oct=6, sus=1)

    # See a list of possible keyword arguments
    print Player.Attributes()
    ```

    Using the `play` SynthDef
    -------------------------

    There is a special case SynthDef object called `play` which allows you
    to play short audio files rather than specify pitches. In this case
    you use a string of characters as the first argument where each character
    refers to a different folder of audio files. You can see more information
    by evaluating `print Samples`. The following line of code creates
    a basic drum beat:

    ```python
    d1 >> play("x-o-")
    ```

    To play multiple patters simultaneously, just create a new `play` object.

    ```python
    bd >> play("x( x)  ")
    hh >> play("---[--]")
    sn >> play("  o ")
    ```

    Grouping characters in round brackets laces the pattern so that on each
    play through of the sequence of samples, the next character in the group's
    sample is played. The sequence `(xo)---` would be played back as if it
    were entered `x---o---`. Using square brackets will force the enclosed samples
    to played in the same time span as a single character e.g. `--[--]` will play
    two hi-hat hits at a half beat then two at a quarter beat. You can play a
    random sample from a selection by using curly braces in your Play String
    like so:

    ```
    d1 >> play("x-o{-[--]o[-o]}")
    ```
    

"""

from os.path import dirname
from random import shuffle, choice
from copy import copy, deepcopy

from Settings import SamplePlayer
from Code import WarningMsg
from SCLang.SynthDef import SynthDefProxy, SynthDef
from Effects import FxList
from Repeat import *
from Patterns import *
from Midi import *
from Root import Root
from Scale import Scale

from Bang import Bang

import Buffers
import TimeVar

Samples = Buffers.BufferManager()

class Player(Repeatable):

    # Set private values

    __vars = []
    __init = False

    # These are used by FoxDot
    keywords   = ('degree', 'oct', 'freq', 'dur', 'delay',
                  'blur', 'amplify', 'scale', 'bpm', 'sample')

    # Base attributes
    base_attributes = ('sus', 'fmod', 'vib', 'slide', 'slidefrom',
                       'pan', 'rate', 'amp', 'room', 'buf', 'bits',)
    
    fx_attributes   = FxList.kwargs()

    metro = None
    server = None

    # Tkinter Window
    widget = None

    default_scale = Scale.default()
    default_root  = Root.default()


    def __init__( self ):

        # Inherit

        Repeatable.__init__(self)
    
        # General setup
        
        self.synthdef = None
        self.id = None
        self.quantise = False
        self.stopping = False
        self.stop_point = 0
        self.following = None
        self.queue_block = None
        self.playstring = ""
        self.char = PlayerKey("", parent=self)
        self.buf_delay = []

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

        self.__vars = self.__dict__.keys()
        self.__init = True

        self.reset()

    # Class methods

    @classmethod
    def Attributes(cls):
        return cls.keywords + cls.base_attributes + cls.fx_attributes

    # Player Object Manipulation
    
    def __rshift__(self, other):
        """ The PlayerObject Method >> """
        
        if isinstance(other, SynthDefProxy):
            self.update(other.name, other.degree, **other.kwargs)
            self + other.mod
            for method, arguments in other.methods.items():
                args, kwargs = arguments
                getattr(self, method).__call__(*args, **kwargs)                
            return self
        
        raise TypeError("{} is an innapropriate argument type for PlayerObject".format(other))
        return self

    def __setattr__(self, name, value):
        if self.__init:

            # Force the data into a TimeVar or Pattern if the attribute is used with SuperCollider
            if name not in self.__vars:

                value = asStream(value) if not isinstance(value, (PlayerKey, TimeVar.var)) else value

                # Update the attribute dict
                self.attr[name] = value

                # Update the current event
                self.event[name] = modi(value, self.event_index)

                #  Make sure the object's dict uses PlayerKey instances

                if name not in self.__dict__:

                    self.__dict__[name] = PlayerKey(self.event[name], parent=self)

                elif not isinstance(self.__dict__[name], PlayerKey):

                    self.__dict__[name] = PlayerKey(self.event[name], parent=self) 

                else:

                    self.__dict__[name].update(self.event[name])
                    
                return
            
        self.__dict__[name] = value
        return

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self is other

    # --- Startup methods

    def reset(self):

        # Add all keywords to the dict, then set non-zero defaults

        for key in Player.Attributes():

            if key != "scale":

                self.attr[key] = asStream(0)

                if key not in self.__dict__:

                    self.__dict__[key] = PlayerKey(0, parent=self)

                elif not isinstance(self.__dict__[key], PlayerKey):

                    self.__dict__[key] = PlayerKey(0, parent=self) 

                else:

                    self.__dict__[key].update(0)

        # --- SuperCollider Keywords

        # Left-Right panning (-1,1)
        self.pan     = 0

        # Sustain
        self.sus     = 1

        # Amplitude
        self.amp     = 1

        # Rate - varies between SynthDef
        self.rate    = 1
        
        # Audio sample buffer number
        self.buf     = 0

        # Reverb
        self.verb   = 0.25
        self.room   = 0.00

        # Frequency modifier
        self.fmod   =  0

        # Buffer
        self.sample  = 0

        # Frequency / rate modifier
        self.slide     = 0
        self.slidefrom = 1

        # --- FoxDot Keywords
        
        # Duration of notes
        self.dur     = 0.5 if self.synthdef == SamplePlayer else 1
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

        # Modifier dict
        
        self.modf = dict([(key, [0]) for key in self.attr])
        
        return self

    # --- Update methods

    def __call__(self, **kwargs):

        # If stopping, kill the event

        if self.stopping and self.metro.now() >= self.stop_point:
            self.kill()
            return

        # If the duration has changed, work out where the internal markers should be

        if self.dur_updated() or kwargs.get("count", False) is True:

            try:

                self.event_n, self.event_index = self.count()

            except TypeError:

                print("TypeError: Innappropriate argument type for 'dur'")

            self.old_dur = self.attr['dur']

        # Get the current state

        dur = 0

        while True:

            self.get_event()

            # Set a 'None' to 0

            if self.event['dur'] is None:

                dur = 0

            # If there are more than one dur (happens sometimes because of threading), only use first
            # This is a temporary solution <-- TODO

            try:

                if len(self.event['dur']) > 0:

                    self.event['dur'] = self.event['dur'][0]                    

            except TypeError:

                pass

            finally:

                if isinstance(self.event['dur'], TimeVar.var):

                    dur = float(self.event['dur'].now(self.event_index))

                else:

                    dur = float(self.event['dur'])

            # Skip events with durations of 0

            if dur == 0:

                self.event_n += 1

            else:

                break

        # Play the note

        if self.metro.solo == self and kwargs.get('verbose', True) and type(self.event['dur']) != rest: 

            if self.synthdef != SamplePlayer:

                self.freq = self.calculate_freq()

            self.send()

        # If using custom bpm

        if self.event['bpm'] is not None:

            try:

                tempo_shift = float(self.metro.bpm) / float(self.event['bpm'])

            except (AttributeError, TypeError):

                tempo_shift = 1

            dur *= tempo_shift

        # Schedule the next event

        self.event_index = self.event_index + dur

        self.metro.schedule(self, self.event_index, kwargs={})

        # Change internal marker

        self.event_n += 1 if not self.reversing else -1
        self.notes_played += 1

        return

    def count(self, time=None):

        # Count the events that should have taken place between 0 and now()

        n = 0
        acc = 0
        dur = 0
        now = (time if time is not None else self.metro.now()) + self.metro.get_latency()

        durations = self.rhythm()
        total_dur = float(sum(durations))

        if total_dur == 0:

            WarningMsg("Player object has a total duration of 0. Set to 1")

            durations = [1]
            total_dur =  1 
            self.dur  =  1
    
        acc = now - (now % total_dur)

        try:

            n = int(len(durations) * (acc / total_dur))

        except TypeError as e:

            WarningMsg(e)

            self.stop()

            return 0, 0

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

    def update(self, synthdef, degree, **kwargs):

        # SynthDef name
        
        self.synthdef = synthdef

        if self.isplaying is False:

            self.reset() # <--

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

            self.dur = kwargs['dur']

            if "sus" not in kwargs and synthdef != SamplePlayer:

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

            # TODO -- play the player early or later than the bar if they're offbeat for example?
            
            next_bar = self.metro.next_bar()
            self.event_n = 0

            self.event_n, self.event_index = self.count(next_bar)
            
            self.metro.schedule(self, self.event_index)

        return self

    def dur_updated(self):
        dur_updated = self.attr['dur'] != self.old_dur
        if self.synthdef == SamplePlayer:
            dur_updated = (self.pattern_rhythm_updated() or dur_updated)
        return dur_updated

    def step_duration(self):
        return 0.5 if self.synthdef is SamplePlayer else 1    


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
                    return Samples.bufnum(self.now('buf')) == other
                raise TypeError("Argument should be a one character string")
            except:
                return False
        else:
            try:
                return Samples.bufnum(self.now('buf'))
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

                print now['degree'], modi(now['degree'], i)

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

    def stutter(self, n=2, **kwargs):
        """ Plays the current note n-1 times. You can specify some keywords,
            such as dur, sus, and rate. """

        if self.metro.solo == self and n > 0:

            dur = float(kwargs.get("dur", self.dur)) / int(n)

            delay = 0

            size = self.largest_attribute()

            for stutter in range(1, n):

                delay += dur

                # Use a custom attr dict and specify the first delay to play "immediately"

                sub = {kw:modi(val, stutter-1) for kw, val in kwargs.items() + [("send_now", True)]}

                self.metro.schedule(func_delay(self.send,  **sub), self.event_index + delay)
                
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
        """ Returns the length of the largest nested tuple in the current event dict """

        exclude = None # debug

        size = len(self.attr['freq'])

        for attr, value in self.event.items():
            if attr != exclude:
                l = get_expanded_len(value)
                if l > size:
                    size = l
        return size

    # --- Methods for preparing and sending OSC messages to SuperCollider

    def now(self, attr="degree", x=0):
        """ Calculates the values for each attr to send to the server at the current clock time """

        modifier_event_n = self.event_n

        attr_value = self.attr[attr]

        # If we are referencing other players' values, make sure they're updated first

        if isinstance(attr_value, PlayerKey):
            
            if attr_value.parent in self.queue_block.objects() and attr_value.parent is not self:

                self.queue_block.call(attr_value.parent, self)

        else:

            attr_value = modi(asStream(attr_value), self.event_n + x)
        
        # If the attribute isn't in the modf dictionary, default to 0

        modf_value = modi(self.modf[attr], modifier_event_n + x) if attr in self.modf else 0

        # Combine attribute and modifier values

        if self.synthdef == SamplePlayer and attr == "degree":

            # Don't bother trying to add values to a play string...?

            pass

        else:

            try:

    ##            if attr == "dur" and type(attr_value) == rest:
    ##
    ##                value = rest(attr_value + modf_value)
    ##
    ##            else:
                
                value = attr_value + modf_value

            except TypeError:

                pass

        return attr_value

    def get_event(self):
        """ Returns a dictionary of attr -> now values """

        # Get the current event

        # self.event = {}

        attributes = copy(self.attr)
        
        for key in attributes:

            # Eg. sp.sus returns the currently used value for sustain

            value = self.event[key] = self.now(key)

            #  Make sure the object's dict uses PlayerKey instances

            if key not in self.__dict__:

                self.__dict__[key] = PlayerKey(value, parent=self)

            elif not isinstance(self.__dict__[key], PlayerKey):

                self.__dict__[key] = PlayerKey(value, parent=self) 

            else:

                self.__dict__[key].update(value)

        # Special case: sample player

        if self.synthdef == SamplePlayer:

            try:

                event_dur = float(self.event['dur'])

                event = self.event['degree'].now() if hasattr(self.event['degree'], "now") else self.event['degree']

                # Store a "char" variable

                size = self.largest_attribute()
                
                event_buf = list(range(size))

                if isinstance(event, PlayGroup):

                    # Nest the Play Group
                    
                    buf_list  = [event]
                    
                else:

                    buf_list  = list(event)

                # buf_list is our list of samples to play as characters
                # event_buf is the list of buffer id's

                ##############
                # TODO - Allow for different sample bank IDs in the buffer delay

                self.buf_delay = []
                
                #for i, bufchar in buf_list: # This should iter over largest event?

                for i in range(size):

                    # Get the char / group from the buf_list

                    bufchar = modi(buf_list, i)

                    # If it is a group

                    if isinstance(bufchar, PlayGroup):

                        # Get the first character, then "delay" the rest

                        self.__dict__['char'].update(bufchar[0])

                        char = Samples[bufchar[0]]

                        # Get the buffer number to play for this sample bank (char)
                        
                        buf_mod_index = int(modi(self.event['sample'], i))

                        event_buf[i] = char.bufnum(buf_mod_index).bufnum               

                        delay = 0
                    
                        for n, b in enumerate(bufchar[1:]):

                            # If it is a timevar / random play group, get the value

                            if hasattr(b, 'now'):

                                b = b.now()

                            # Get the sample bank / char

                            char = Samples[b]

                            # Find the appropriate sample in the bank

                            buf_mod_index = int(modi(self.event['sample'], i))

                            # Add the delay

                            delay += (bufchar[n].dur * event_dur)

                            # Add it to our delay list

                            self.buf_delay.append((char.bufnum(buf_mod_index),  delay))

                    else:

                        # Get the char / bank

                        char = Samples[bufchar]

                        self.__dict__['char'].update(bufchar)

                        # Get the buffer number to play
                        
                        buf_mod_index = int(modi(self.event['sample'], i))

                        event_buf[i] = char.bufnum(buf_mod_index).bufnum

                self.event['buf'] = P(event_buf)

            except TypeError as e:

                WarningMsg("In Player.get_event",  e)
            
        return self


    def osc_message(self, index=0, **kwargs):
        """ NEW: Creates an OSC packet to play a SynthDef in SuperCollider,
            use kwargs to force values in the packet, e.g. pan=1 will force ['pan', 1] """

        freq = float(modi(self.attr['freq'], index))
        
        message = ['freq',  freq ]
        fx_dict = {}

        attributes = self.attr.copy()

        # Go through the attr dictionary and add kwargs

        for key in attributes:

            try:

                # Don't use fx keywords or foxdot keywords

                if key not in FxList.kwargs() and key not in self.keywords:

                    val = group_modi(kwargs.get(key, self.event[key]), index)

                    # Special case modulation

                    if key == "sus":

                        val = val * self.metro.beat_dur() * modi(kwargs.get('blur', self.event['blur']), index)

                    elif key == "amp":

                        val = val * modi(kwargs.get('amplify', self.event['amplify']), index)

                    message += [key, val]

            except KeyError as e:

                WarningMsg("In osc_message", key, e)

        # See if any fx_attributes 

        for key in self.fx_attributes:

            if key in attributes: 

                # All effects use sustain to release nodes

                fx_dict[key] = []

                # Look for any other attributes require e.g. room and verb

                for sub_key in FxList[key].args:

                    if sub_key in self.event:

                        #for i in range(0, len(message), 2):

                        if sub_key in message:

                            # if sub_key == message[i]:

                            i = message.index(sub_key) + 1

                            # val = modi(kwargs.get(key, self.event[key]), index)

                            val = message[i]

                        else:

                            try:

                                val = group_modi(kwargs.get(sub_key, self.event[sub_key]), index)

                            except TypeError as e:

                                val = 0

                            except KeyError as e:

                                del fx_dict[key]
                                break

                        # Don't send fx with zero values, unless it is a timevar or playerkey i.e. has a "now" attr

                        if val == 0 and not hasattr(val, 'now'):

                            del fx_dict[key]

                            break

                        else:

                            fx_dict[key] += [sub_key, val]

        return message, fx_dict


    def send(self, **kwargs):
        """ Sends the current event data to SuperCollder.
            Use kwargs to overide values in the """

        size = self.largest_attribute()
        banged = False
        sent_messages = []
        delayed_messages = []

        last_msg = None

        for i in range(size):

            osc_msg, effects = self.osc_message(i, **kwargs)

            delay = group_modi(kwargs.get('delay', self.event.get('delay', 0)), i)
            
            buf   = group_modi(kwargs.get('buf', self.event['buf']), i)

            amp   = osc_msg[osc_msg.index('amp') + 1]

            # Any messages with zero amps or 0 buf are not sent <- maybe change that for "now" classes

            if (self.synthdef != SamplePlayer and amp > 0) or (self.synthdef == SamplePlayer and buf > 0 and amp > 0):

                synthdef = self.get_synth_name(buf)

                if delay > 0:

                    # Sometimes there are race conditions, so make sure delay is just one value

                    while hasattr(delay, "__len__"): # <- I think this is why var's don't wory

                        delay = delay[i]

                    if (delay, osc_msg, effects) not in delayed_messages:

                        # Schedule the note to play in the future & to update the playerkeys

                        self.metro.schedule(send_delay(self, synthdef, osc_msg, effects), self.event_index + delay)

                        delayed_messages.append((delay, osc_msg, effects))

                    if self.bang_kwargs:

                        self.metro.schedule(self.bang, self.metro.now() + delay)
                    
                else:

                    # Don't send duplicate messages

                    if (osc_msg, effects) not in sent_messages:

                        # --- New way of sending messages all at once
                    
                        compiled_msg = self.server.sendPlayerMessage(synthdef, osc_msg, effects,)

                        # -- We can specify to send immediately as opposed to all together at the end of the block

                        if kwargs.get("send_now", False):

                            self.server.client.send(compiled_msg)

                        else:

                            self.queue_block.osc_messages.append(compiled_msg)
                        
                        # self.server.sendPlayerMessage(synthdef, osc_msg, effects) -- old way

                        sent_messages.append((osc_msg, effects))
                        
                    if not banged and self.bang_kwargs:

                        self.bang()

                        banged = True

            # Store the last message so we can compare if delayed

            last_msg = (osc_msg, effects)

            # If a sample is specified as in brackets like "[--]" it uses buf_delay
                        
            if self.buf_delay:

                for buf_num, buf_delay in self.buf_delay:

                    # Only send messages with amps > 0

                    i = osc_msg.index('amp') + 1

                    if osc_msg[i] > 0:

                        # Make sure we use an integer number

                        buf_num = int(buf_num)

                        if buf_num > 0:

                            numChannels = Samples.getBuffer(buf_num).channels

                            if numChannels == 1:

                                synthdef = "play1"

                            else:

                                synthdef = "play2"

                            if (buf_delay + delay, osc_msg, effects) not in delayed_messages:

                                i = osc_msg.index('buf') + 1

                                osc_msg[i] = buf_num

                                self.metro.schedule(send_delay(self, synthdef, osc_msg, effects), self.event_index + buf_delay + delay)

                                delayed_messages.append((buf_delay + delay, osc_msg, effects))

                    last_msg = (osc_msg, effects)
            
        return

    def get_synth_name(self, buf=0):
        if self.synthdef == SamplePlayer:
            numChannels = Samples.getBuffer(buf).channels
            if numChannels == 1:
                synthdef = "play1"
            else:
                synthdef = "play2"
        else:
            synthdef = str(self.synthdef)
        return synthdef

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

    def follow(self, lead=False):
        """ Takes a now object and then follows the notes """

        if isinstance(lead, self.__class__):

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
        return self

    def mirror(self):
        if self.synthdef == SamplePlayer:
            self._replace_string(PlayString(self.playstring).mirror())
        else:
            self._replace_degree(self.attr['degree'].mirror())
        return self

    def rotate(self, n=1):
        if self.synthdef == SamplePlayer:
            self._replace_string(PlayString(self.playstring).rotate(n))
        else:
            self._replace_degree(self.attr['degree'].rotate(n))
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

    def changeSynth(self, list_of_synthdefs):
        new_synth = choice(list_of_synthdefs)
        if isinstance(new_synth, SynthDef):
            new_synth = str(new_synth.name)
        self.synthdef = new_synth
        # TODO, change the >> name
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

            print self.bang_kwargs

            bang = Bang(self, self.bang_kwargs)

        return self

####
class PlayerKey(object):
    def __init__(self, value=None, reference=None, parent=None):

        # Reference to the Player object that is using this
        self.parent = parent
        
        self.value = asStream(value)
        self.index = 0
        
        if reference is None:

            self.other   = 0
            self.num_ref = 0

        else:

            self.other   = reference
            self.parent  = reference.parent
            self.num_ref = reference.num_ref + 1
            
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
        new.calculate = Mul
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
        new = PlayerKey(other, self)
        new.calculate = lambda a, b: int(a == b)
        return new
    
    def __ne__(self, other):
        new = PlayerKey(other, self)
        new.calculate = lambda a, b: int(a != b)
        return new
    
    def __gt__(self, other):
        new = PlayerKey(other, self)
        new.calculate = lambda a, b: int(a > b)
        return new
    
    def __lt__(self, other):
        new = PlayerKey(other, self)
        new.calculate = lambda a, b: int(a < b)
        return new
    
    def __ge__(self, other):
        new = PlayerKey(other, self)
        new.calculate = lambda a, b: int(a >= b)
        return new
    
    def __le__(self, other):
        new = PlayerKey(other, self)
        new.calculate = lambda a, b: int(a <= b)
        return new

    def __nonzero__(self):
        """ TODO - is this versatile? """
        return int(self.now())

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
    def __init__(self, p, synthdef, message, fx={}):
        self.master = p
        self.server = p.server
        self.synth = synthdef
        self.msg = list(message[:])
        self.fx = {}
        self.update_dict = {}
        self.queue_block = None
        # Store a dict of values to update the player with when called
        for key, value in fx.items():
            osc = []
            for i in range(0, len(value), 2): # an osc message
                self.update_dict[str(value[i])] = value[i+1]
                osc += [str(value[i]), value[i+1]]
            self.fx[str(key)] = osc
        for i in range(0, len(self.msg), 2):
            self.update_dict[str(self.msg[i])] = self.msg[i+1]
        # ---
    def __repr__(self):
        return "<'{}' delay>".format(self.synth)
    def __call__(self):
        for key, value in self.update_dict.items():
            self.master.__dict__[key].update(value)
            if key == "buf" and value != 0:
                self.master.__dict__["char"].update( Samples.getBuffer(value).char )
        compiled_msg = self.server.sendPlayerMessage(self.synth, self.msg, self.fx)
        self.queue_block.osc_messages.append(compiled_msg)
        return
        

class func_delay:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args[:]
        self.kwargs = kwargs.copy()
    def __repr__(self):
        return "<'{}' delay>".format(self.func.__name__)
    def __call__(self):
        self.func(*self.args, **self.kwargs)


###### GROUP OBJECT

class Group:

    def __init__(self, *args):

        self.players = args

    def __len__(self):
        return len(self.players)

    def __str__(self):
        return str(self.players)

    def iterate(self, dur=4):
        if dur == 0 or dur is None:
            self.amplify=1
        else:
            delay, on = 0, float(dur) / len(self.players)
            for player in self.players:
                player.amplify=TimeVar.var([0,1,0],[delay, on, dur-delay])
                delay += on
        return           

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

class rest(object):
    ''' Represents a rest when used with a Player's `dur` keyword
    '''
    def __init__(self, dur=1):
        self.dur = dur
    def __repr__(self):
        return "<rest: {}>".format(self.dur)
    def __add__(self, other):
        return rest(self.dur + other)
    def __radd__(self, other):
        return rest(other + self.dur)
    def __sub__(self, other):
        return rest(self.dur - other)
    def __rsub__(self, other):
        return rest(other - self.dur)
    def __mul__(self, other):
        return rest(self.dur * other)
    def __rmul__(self, other):
        return rest(other * self.dur)
    def __div__(self, other):
        return rest(self.dur / other)
    def __rdiv__(self, other):
        return rest(other / self.dur)
    def __truediv__(self, other):
        return rest(float(self.dur) / other)
    def __rtruediv__(self, other):
        return rest(other / float(self.dur))
    def __mod__(self, other):
        return rest(self.dur % other)
    def __rmod__(self, other):
        return rest(other % self.dur)
    def __int__(self):
        return int(self.dur)
    def __float__(self):
        return float(self.dur)
