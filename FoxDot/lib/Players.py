"""    
    Players are what make FoxDot make music. They are similar in design to
    SuperCollider's `PDef` and `PBind` combo but with slicker syntax. FoxDot
    uses SuperCollider to *actually* make the sound and does so by triggering
    predefined `SynthDefs` - sort of like definitions of a digital instruments.
    To have a look at the list of `SynthDefs`, you can just `print` them to
    the console: ::

        print(SynthDefs)

    Each one of these represents a `SynthDef` *object*. These objects are then
    given to Players to play - like giving an instrument to someone in your
    orchestra. To give someone the instrument, `pads`, you use a double arrow
    some code syntax like this: ::

        p1 >> pads()

    To stop a Player, use the `stop` method e.g. `p1.stop()`. If you want to
    stop all players, you can use the command `Clock.clear()` or the keyboard
    shortcut `Ctrl+.`, which executes this command.

    `p1` is the name of a predefined player object. At startup, FoxDot reserves
    all one- and two-character variable names, such as `x`, `p1`, or `bd` for
    player objects but these can be repurposed if you like. If you want to use
    a variable name for a player object with more than two characters, you just
    instantiate a new `Player` object: ::

        foo = Player()

        foo >> pads()

    Changing parameters
    -------------------

    By default, player objects play the first note of their default scale (more
    below) with a duration of 1 beat per note. To change the pitch just give the
    `SynthDef` a list of numbers. ::

        p1 >> pads([0,7,6,4])

    Play multiple pitches together by putting them in round brackets: ::

        p1 >> pads([0,2,4,(0,2,4)])
    
    When you start FoxDot up, your clock is ticking at 120bpm and your player
    objects are all playing in the major scale. With 8 pitches in the major scale,
    the 0 refers to the first pitch and the 7 refers to the pitch one octave
    higher because Python, like most programming languages, uses zero-indexing.
    To change your scale you can specify a new scale as a keyword argument (see
    the documentation on `Scales` for more information on scales) or change the
    default scale for all player objects. ::

        # Changing scale as a keyword argument
        p1 >> pads([0,7,6,4], scale=Scale.minor)

        # Changing the default scalew (the following are equivalent)
        Scale.default.set("minor")
        Scale.default.set(Scale.minor)
        Scale.default.set([0,2,3,5,7,8,10])

        # See a list of scales
        print Scale.names()

        # Change the tempo (this takes effect at the next bar)
        Clock.bpm = 144

    To change the rhythm of your player object, specify the durations using
    the `dur` keyword. Other keywords can be specified, such as `oct` for the
    octave and `sus` for the sustain, which is the same as the duration by
    default. ::

        p1 >> pads([0,7,6,4], dur=[1,1/2,1/4,1/4], oct=6, sus=1)

        # See a list of possible keyword arguments
        print(Player.get_attributes())

    Using the `play` SynthDef
    -------------------------

    There is a special case SynthDef object called `play` which allows you
    to play short audio files rather than specify pitches. In this case
    you use a string of characters as the first argument where each character
    refers to a different folder of audio files. You can see more information
    by evaluating `print(Samples)`. The following line of code creates
    a basic drum beat: ::

        d1 >> play("x-o-")

    To play multiple patterns simultaneously, you can create a new `play` object. This
    is useful if you want to have different attributes for each player. ::
        
        bd >> play("x( x)  ", dur=1)
        hh >> play("---[--]", dur=[1/2,1/2,1/4], rate=4)
        sn >> play("  o ", rate=(.9,1), pan=(-1,1))

    Grouping characters in round brackets laces the pattern so that on each
    play through of the sequence of samples, the next character in the group's
    sample is played. The sequence `(xo)---` would be played back as if it
    were entered `x---o---`. Using square brackets will force the enclosed samples
    to played in the same time span as a single character e.g. `--[--]` will play
    two hi-hat hits at a half beat then two at a quarter beat. You can play a
    random sample from a selection by using curly braces in your Play String
    like so: ::

        d1 >> play("x-o{-[--]o[-o]}")

    FoxDot Player Object Keywords
    -----------------------------

    dur - Durations (defaults to 1 and 1/2 for the Sample Player)

    sus - Sustain (defaults to `dur`)

    amp - Amplitude (defaults to 1)

    rate - Variable keyword used for misc. changes to a signal. E.g. Playback rate of the Sample Player (defaults to 1)

    delay - A duration of time to wait before sending the information to SuperCollider (defaults to 0)

    sample - Special keyword for Sample Players; selects another audio file from the bank of samples for a sample character.
    

"""

from __future__ import absolute_import, division, print_function

import itertools
from functools import partial

from os.path import dirname
from random import shuffle, choice
from copy import copy, deepcopy

from .Settings import SamplePlayer, LoopPlayer
from .Code import WarningMsg, debug_stdout
from .SCLang.SynthDef import SynthDefProxy, SynthDef, SynthDefs
from .Effects import FxList
from .Utils import stdout
from .Buffers import Samples

from .Key import *
from .Repeat import *
from .Patterns import *
# from .Midi import *

from .Root import Root
from .Scale import Scale, ScaleType, ScalePattern
from .Scale import midi, miditofreq, get_freq_and_midi

from .Bang import Bang

from .TimeVar import TimeVar, Pvar

class EmptyPlayer(object):
    """ Place holder for Player objects created at run-time to reduce load time.
    """
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "<{} - Unassigned>".format(self.name)
    
    def __rshift__(self, *args, **kwargs):
        """ Converts an EmptyPlayer to a Player. """
        self.__class__ = Player
        self.__init__(self.name)
        self.__rshift__(*args, **kwargs)
        return self

    def __invert__(self):
        return self.reset()

    def __getattribute__(self, name):
        """ Tries to return the correct attr; if not init the Player and try again """
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            self.__class__ = Player
            self.__init__(self.name)
            try:
                return self.__getattribute__(name)
            except AttributeError:
                return self.__getattr__(name) # use getattr to make sure we return player key


class Player(Repeatable):

    """
    FoxDot generates music by creating instances of `Player` and giving them instructions
    to follow. At startup FoxDot creates many instances of `Player` and assigns them to
    any valid two character variable. This is so that when you start playing you don't 
    have to worry about typing `myPlayer = Player()` and `myPlayer_2 = Player()` every
    time you want to do something new. Of course there is nothing stopping you from 
    doing that if yo so wish.

    Instances of `Player` are given instructions to generate music using the `>>` syntax,
    overriding the bitshift operator, and should be given an instance of `SynthDefProxy`.
    A `SynthDefProxy` is created when calling an instance of `SynthDef` - these are the
    "instruments" used by player objects and are written in SuperCollider code. You can
    see more information about these in the `SCLang` module. Below describes how to assign
    a `SynthDefProxy` of the `SynthDef` `pads` to a `Player` instance called `p1`: ::

        # Calling pads as if it were a function returns a 
        # pads SynthDefProxy object which is assigned to p1
        p1 >> pads()

        # You could store several instances and assign them at different times
        proxy_1 = pads([0,1,2,3], dur=1/2)
        proxy_2 = pads([4,5,6,7], dur=1)

        p1 >> proxy_1 # Assign the first to p1
        p1 >> proxy_2 # This replaces the instructions being followed by p1
    """

    # Set private values

    debug = 0

    __vars = []
    __init = False

    # Really need to tidy this up

    keywords   = ('degree', 'oct', 'freq', 'dur', 'delay', 'buf',
                  'blur', 'amplify', 'scale', 'bpm', 'sample', "env")

    envelope_keywords = ("atk", "decay", "rel", "legato", "curve", "gain")

    # Base attributes
    
    base_attributes = ('sus', 'fmod', 'pan', 'rate', 'amp', 'midinote', 'channel') 

    required_keys = ("amp", "sus")
    
    internal_keywords = tuple(value for value in keywords if value != "degree")

    # Aliases

    alias = { "pitch" : "degree",
              "char"  : "degree" }

    fx_attributes = FxList.all_kwargs()
    fx_keys       = FxList.kwargs()

    # Load default sample bank
    samples = Samples

    # Set in __init__.py
    metro   = None

    default_scale = Scale.default

    default_root  = Root.default() # TODO//remove callable

    after_update_methods = ["stutter"]

    # Tkinter Window
    widget = None

    def __init__(self, name=None):

        # Inherit from repeatable i.e. x.every

        Repeatable.__init__(self)

        self.method_synonyms["->"] = "rshift"
        self.method_synonyms["<-"] = "lshift"
    
        # General setup
        
        self.synthdef = None
        self.id = name

        #self.current_event_size   = 0
        #self.current_event_length = 0
        #self.current_event_depth  = 0

        # Stopping flag
        self.stopping = False
        self.stop_point = 0

        # Reference to other objects in the clock played at the same time
        self.queue_block = None
        self.bus = None

        # The string representation of the degree of the player
        self.playstring = ""

        # Information used in generating OSC messages
        self.buf_delay = []
        self.timestamp = 0
        # self.condition = lambda: True
        # self.sent_messages = []

        # Visual feedback information

        self.envelope    = None
        self.line_number = None
        self.whitespace  = None
        self.do_bang     = False
        self.bang_kwargs = {}

        # Keeps track of which note to play etc

        self.event_index = 0
        self.event_n = 0
        self.notes_played = 0
        self.event = {}
        self.accessed_keys = []

        # Used for checking clock updates

        self.current_dur = None
        self.old_pattern_dur = None
        self.old_dur = None
        
        self.isplaying = False
        self.isAlive = True

        # These dicts contain the attribute and modifier values that are sent to SuperCollider     

        self.attr  = {}
        self.modifier = Pattern()
        self.mod_data = 0
        self.filename = None

        # Keyword arguments that are used internally

        self.scale = None
        self.offset  = 0
        self.following = None
        
        # List the internal variables we don't want to send to SuperCollider

        self.__vars = list(self.__dict__.keys())
        self.__init = True

        self.reset()

    # Class methods

    @classmethod
    def help(cls):
        return print(cls.__doc__)

    @classmethod
    def get_attributes(cls):
        """ Returns a list of possible keyword arguments for FoxDot players and effects """
        return cls.keywords + cls.base_attributes + cls.fx_attributes

    @classmethod
    def Attributes(cls):
        """ To be replaced by `Player.get_attributes()` """
        return cls.get_attributes()

    @classmethod
    def set_clock(cls, tempo_clock):
        cls.metro = tempo_clock

    # Should this also be instance method?
    @classmethod
    def set_sample_bank(cls, sample_bank):
        cls.samples = sample_bank

    def __hash__(self):
        return hash(self.id) # could be problematic if there are id clashes?

    # Player Object Manipulation
    
    def __rshift__(self, other):
        """ Handles the allocation of SynthDef objects using >> syntax, other must be
            an instance of `SynthDefProxy`, which is usually created when calling a
            `SynthDef`
        """
        
        if isinstance(other, SynthDefProxy):
            
            # Call the update method
            
            self.update(other.name, other.degree, **other.kwargs)
        
            # self.update_pattern_root('sample' if self.synthdef == SamplePlayer else 'degree')
            
            for method, arguments in other.methods:
            
                args, kwargs = arguments
            
                getattr(self, method).__call__(*args, **kwargs)
            
            # Add the modifier (check if not 0 to stop adding 0 to values)

            if (not isinstance(other.mod, (int, float))) or (other.mod != 0):

                self + other.mod
            
            return self
        
        raise TypeError("{} is an innapropriate argument type for PlayerObject".format(other))

        return self

    def test_for_circular_reference(self, value, attr, last_player=None, last_attr=None):
        """ Used to raise an exception if a player's attribute refers to itself e.g. `p1 >> pads(dur=p1.dur)` """

        # We are setting self.attr to value, check if value depends on self.attr

        if isinstance(value, PGroup):

            for item in value:

                self.test_for_circular_reference(item, attr, last_player, last_attr)

        elif isinstance(value, PlayerKey):

            # If the Player key relies on this player.attr, raise error

            if value.cmp(self, attr):

                ident_self = value.name()

                if last_player is not None:

                    ident_other = "{}.{}".format(last_player.id, last_attr)

                else:

                    ident_other = ident_self

                err = "Circular reference found: {} to itself via {}".format(ident_self, ident_other)

                raise ValueError(err)

            elif last_player == value.player and last_attr == value.attr:

                return

            else:

                # Go through the player key's 

                for item in value.get_player_attribute():
            
                    self.test_for_circular_reference(item, attr, value.player, value.attr)

        return

    def __setattr__(self, name, value):

        # Possibly replace with slots?

        if self.__init:

            # Force the data into a Pattern if the attribute is used with SuperCollider
            
            if name not in self.__vars:

                # Get any alias

                name = self.alias.get(name, name)

                value = asStream(value)

                for item in value:

                    self.test_for_circular_reference(item, name)

                # Update the attribute dict if no error
                
                self.attr[name] = value

                # Remove from the stored pattern dict / call those

                self.update_pattern_root(name)

                # keep track of what values we change with +-

                if (self.synthdef == SamplePlayer and name == "sample") or (self.synthdef != SamplePlayer and name == "degree"):

                    self.modifier = value

                # Update any playerkey

                if name in self.__dict__:

                    if isinstance(self.__dict__[name], PlayerKey):

                        self.__dict__[name].update_pattern()

                # self.update_player_key(name, 0, 0)

                return
            
        self.__dict__[name] = value

        return

    def __getattr__(self, name):
        try:
            # This checks for aliases, not the actual keys
            name = self.alias.get(name, name)

            if name in self.attr and name not in self.__dict__:

                # Return a Player key

                self.update_player_key(name, self.now(name), 0)

            item = self.__dict__[name]

            # If returning a player key, keep track of which are being accessed
        
            if isinstance(item, PlayerKey) and name not in self.accessed_keys:                
        
                self.accessed_keys.append(name)
            
            return item
        
        except KeyError:
            
            err = "Player Object has no attribute '{}'".format(name)
            
            raise AttributeError(err)

        return

    def __getattribute__(self, name):
        # This checks for aliases, not the actual keys
        name = Player.alias.get(name, name)
        item = object.__getattribute__(self, name)
        if isinstance(item, PlayerKey):
            if name not in self.accessed_keys:
                self.accessed_keys.append(name)
        return item

    def __getitem__(self, name):
        if self.__init:
            if name not in self.__vars:
                return self.attr[name]
            pass
        return self.__dict__[name]

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self is other

    # --- Startup methods

    def reset(self):
        """ Sets all Player attributes to 0 unless their default is specified by an effect. Also
            can be called by using a tilde before the player variable. E.g. ~p1 """

        # Add all keywords to the dict, then set non-zero defaults

        reset = []

        for key in Player.Attributes():

            if key not in ("scale", "dur", "sus", "blur", "amp",
                            "amplify", "degree", "oct", "bpm"):

                setattr(self, key, 0)

            reset.append(key)

        # Set any non zero defaults for effects, e.g. verb=0.25

        for key in Player.fx_attributes:

            value = FxList.defaults[key]

            setattr(self, key, value)

            reset.append(key)

        # Set SynthDef defaults

        if self.synthdef in SynthDefs:

            synth = SynthDefs[self.synthdef]
            
            for key in ("atk", "decay", "rel"):

                setattr(self, key, synth.defaults[key])

                reset.append(key)

        # Any other attribute that might have been used - set to 0

        for key in self.attr:

            if key not in reset:

                setattr(self, key, 0)

        # Set any non-zero values for FoxDot

        # Sustain & Legato
        self.sus     = 0.5 if self.synthdef == SamplePlayer else 1
        self.blur    = 1

        # Amplitude
        self.amp     = 1
        self.amplify = 1

        # Duration of notes
        self.dur     = 0.5 if self.synthdef == SamplePlayer else 1

        # Degree of scale / Characters of samples
        self.degree  = " " if self.synthdef is SamplePlayer else 0

        # Octave of the note
        self.oct     = 5
        
        # Tempo
        self.bpm     = None

        # Stop calling any repeating methods

        self.stop_calling_all()
        
        return self

    def __invert__(self):
        """ Using the ~ syntax resets the player """
        return self.reset()

    # --- Update methods

    def __call__(self, **kwargs):
        """ Sends the next osc message event to SuperCollider and schedules this
            Player in the clock based on the current clock time and this player's
            current duration value. """

        # If stopping, kill the event

        if self.stopping and self.metro.now() >= self.stop_point:
            
            self.kill()
            
            return

        # If the duration has changed, work out where the internal markers should be

        # -- This could be in its own private function

        force_count = kwargs.get("count", False)
        dur_updated = self.dur_updated() 

        if dur_updated or force_count is True:

            try:

                self.event_n, self.event_index = self.count(self.event_index if not force_count else None)

            except TypeError as e:

                print(e)

                print("TypeError: Innappropriate argument type for 'dur'")

        # Get the current state 

        self.get_event() 

        # Play the note
        
        if not isinstance(self.event["dur"], rest):

            try:
        
                self.send(verbose=(self.metro.solo == self and kwargs.get('verbose', True)))

            except Exception as err:

                print("Error in Player {}: {}".format(self.id, err))
        
        # If using custom bpm

        dur = self.event["dur"]

        if self.event['bpm'] is not None:

            try:

                tempo_shift = float(self.metro.bpm) / float(self.event['bpm'])

            except (AttributeError, TypeError, ZeroDivisionError):

                tempo_shift = 1

            dur *= tempo_shift

        # Schedule the next event (could move before get_event and use the index for get_event)

        self.event_index = self.event_index + dur

        self.metro.schedule(self, self.event_index, kwargs={})

        # Change internal marker

        self.event_n += 1 
        self.notes_played += 1

        return

    def count(self, time=None, event_after=False):
        """ Counts the number of events that will have taken place between 0 and `time`. If
            `time` is not specified the function uses self.metro.now(). Setting `event_after`
            to `True` will find the next event *after* `time`"""

        n = 0
        acc = 0
        dur = 0
        now = (time if time is not None else self.metro.now())

        if self.current_dur is None:

            self.current_dur = self.rhythm()

        durations = list(map(get_first_item, self.current_dur)) # careful here
        
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

        if acc != now:

            while True:

                dur = float(modi(durations, n))

                if acc + dur == now:

                    acc += dur

                    n += 1

                    break

                elif acc + dur > now:

                    if event_after:

                        acc += dur
                        n += 1

                    break

                else:
                    
                    acc += dur
                    n += 1

        # Returns value for self.event_n and self.event_index

        return n, acc

    def dur_updated(self):
        """ Returns True if the players duration has changed since the last call """
        self.current_dur = self.rhythm()
        if self.current_dur != self.old_dur:
            self.old_dur = self.current_dur
            return True
        return False

    def rhythm(self):
        """ Returns the players array of durations at this point in time """
        return list(map(lambda x: x if isinstance(x, (int, float)) else self.unpack(x), self.attr["dur"]))

    def update(self, synthdef, degree, **kwargs):
        """ Updates the attributes of the player. Called using the >> syntax.
        """

        # SynthDef name
        
        self.synthdef = synthdef

        # Make sure all values are reset to start

        if "filename" in kwargs:

            self.filename = kwargs["filename"]
            del kwargs["filename"]

        if self.isplaying is False:

            self.reset() 

        # If there is a designated solo player when updating, add this at next bar
        
        if self.metro.solo.active() and self.metro.solo != self:

            self.metro.schedule(lambda *args, **kwargs: self.metro.solo.add(self), self.metro.next_bar())

        # Update the attribute values

        special_cases = ["scale", "root", "dur"]

        # Set the degree

        if synthdef == SamplePlayer:

            if type(degree) == str:

                self.playstring = degree

            else:

                self.playstring = None

            if degree is not None:

                setattr(self, "degree", degree if degree != "" else " ")

        elif degree is not None:

            self.playstring = str(degree) # this doesn't work for var!

            setattr(self, "degree", degree)

        else:

            setattr(self, "degree", 0)            


        # Set special case attributes

        self.scale = kwargs.get("scale", self.__class__.default_scale )
        self.root  = kwargs.get("root",  self.__class__.default_root )

        # If only duration is specified, set sustain to that value also

        if "dur" in kwargs:

            # If we use tuples / PGroups in setting duration, use it to modify delay using the PDur algorithm

            setattr(self, "dur", kwargs["dur"])

            if "sus" not in kwargs:

                self.sus = self.attr['dur']

        # Set any other attributes

        for name, value in kwargs.items():

            if name not in special_cases:

                setattr(self, name, value)

        # Calculate new position if not already playing

        if self.isplaying is False:

            # Add to clock
            
            self.isplaying = True
            self.stopping = False

            # If we want to update now, set the start point to now

            after = True

            if self.metro.now_flag:

                start_point = self.metro.now()

                after = False

            elif kwargs.get("quantise", True) == False:

                start_point = self.metro.now()

            else:
            
                start_point = self.metro.next_bar()

            self.event_n = 0

            self.event_n, self.event_index = self.count(start_point, event_after=after)

            self.metro.schedule(self, self.event_index)

        return self

    def often(self, *args, **kwargs):
        """ Calls a method every 1/2 to 4 beats using `every` """
        return self.every(PRand(1, 8)/2, *args, **kwargs)

    def sometimes(self, *args, **kwargs):
        """ Calls a method every 4 to 16 beats using `every` """
        return self.every(PRand(8, 32)/2, *args, **kwargs)

    def rarely(self, *args, **kwargs):
        """ Calls a method every 16 to 32 beats using `every` """
        return self.every(PRand(32, 64)/2, *args, **kwargs)

    def get_timestamp(self, beat=None):
        if beat is not None:
            timestamp = self.metro.osc_message_time() - self.metro.beat_dur(self.metro.now() - beat)
        else:
            timestamp = self.metro.osc_message_time()
        return timestamp

    def stutter(self, amount=None, _beat_=None, **kwargs):
        """ Plays the current note n-1 times. You can specify keywords. """

        timestamp = self.get_timestamp(_beat_)
        
        # Get the current values (this might be called between events)

        n = int(kwargs.get("n", amount if amount is not None else 2))
        ahead = int(kwargs.get("ahead", 0))

        for key in ("ahead", "n"):
            if key in kwargs:
                del kwargs[key]

        # Only send if n > 1 and the player is playing

        if self.metro.solo == self and n > 1:

            new_event = {}

            attributes = self.attr.copy()
        
            attr_keys = set(list(self.attr.keys()) + list(kwargs.keys()))
            
            for key in attr_keys:

                if key in kwargs:

                    item = kwargs[key]

                    if isinstance(item, PGroupPrime):

                        new_event[key] = self.unpack(item)

                    elif isinstance(item, PGroup):

                        new_event[key] = self.unpack(PGroup([item]))

                    else:

                        new_event[key] = self.unpack(PGroup(item))

                elif len(attributes[key]) > 0:

                    new_event[key] = self.now(key, ahead)

            new_event = self.unduplicate_durs(new_event)

            dur = float(kwargs.get("dur", new_event["dur"])) / n

            new_event["dur"] = dur

            # Get PGroup delays

            new_event["delay"] = PGroup([dur * (i+1) for i in range(max(n, self.get_event_length(new_event)))])

            new_event = self.get_prime_funcs(new_event)

            self.send(timestamp=timestamp, **new_event)
                
        return self

    def jump(self, ahead=1, _beat_=None, **kwargs):
        """ Plays an event ahead of time. """

        timestamp = self.get_timestamp(_beat_)

        if self.metro.solo == self:

            new_event = {}
        
            attributes = copy(self.attr)
            
            for key in attributes:

                if key in kwargs:

                    new_event[key] = self.unpack(PGroup(kwargs[key]))

                elif len(attributes[key]) > 0:

                    new_event[key] = self.now(key, ahead)

            new_event = self.unduplicate_durs(new_event)

            new_event = self.get_prime_funcs(new_event)

            self.send(timestamp=timestamp, **new_event)
                
        return self

    def lshift(self, n=1):
        """ Plays the event behind """
        self.event_n -= (n+1)
        return self

    def rshift(self, n=1):
        """ Plays the event in front """
        self.event_n += n
        return self

    # Preset methods

    def spread(self, on=0.125):
        """ Sets pan to (-1, 1) and pshift to (0, 0.125)"""
        if on != 0:
            self.pan=(-1,1)
            self.pshift=(0,on)
        else:
            self.pan=0
            self.pshift=0
        return self

    def unison(self, unison=2, detune=0.125):
        """ Like spread(), but can specify number of voices(unison)  
        Sets pan to (-1,-0.5,..,0.5,1) and pshift to (-0.125,-0.0625,...,0.0625,0.125)
        If unison is odd, an unchanged voice is added in the center
        Eg : p1.unison(4, 0.5) => pshift=(-0.5,-0.25,0.25,0.5), pan=(-1.0,-0.5,0.5,1.0)
             p1.unison(5, 0.8) => pshift=(-0.8,-0.4,0,0.4,0.8), pan=(-1.0,-0.5,0,0.5,1.0)
        """
        if unison != 0:
            pan=[]
            pshift=[]
            uni = int(unison if unison%2==0 else unison-1)
            for i in range(1,int(uni/2)+1):
                pan.append(2*i/uni)
                pan.insert(0, -2*i/uni)
            for i in range(1, int(uni/2)+1):
                pshift.append(detune*(i/(uni/2)))
                pshift.insert(0,detune*-(i/(uni/2)))
            if unison%2!=0 and unison > 1:
                pan.insert(int(len(pan)/2), 0)
                pshift.insert(int(len(pan)/2), 0)              
            self.pan = tuple(pan)
            self.pshift = tuple(pshift)
        else:
            self.pan=0
            self.pshift=0
        return self

    def seconds(self):
        """ Sets the player bpm to 60 so duration will be measured in seconds """
        self.bpm=60
        return self
    
    def slider(self, start=0, on=1):
        """ Creates a glissando effect between notes """
        if on:
            if start:
                self.slide=[1,0]
                self.slidefrom=[0,1]
            else:
                self.slide=[0,1]
                self.slidefrom=[1,0]
            self.slidedelay=0.75
        else:
            self.slide=0
            self.slidefrom=0
            self.slidedelay=0
        return self

    def penta(self, switch=1):
        """ Shorthand for setting the scale to the pentatonic mode of the default scale """
        if switch:
            self.scale = self.__class__.default_scale.pentatonic
        else:
            self.scale = self.__class__.default_scale
        return self

    def alt_dur(self, dur):
        """ Used to set a duration that changes linearly over time. You should use a `linvar` but
            any value can be used. This sets the `dur` to 1 and uses the `bpm` attribute to 
            seemingly alter the durations """

        self.dur = 1
        self.bpm = self.metro.bpm*(1/(dur))
        return self

    def reverse(self):
        """ Reverses every attribute stream """
        for attr in self.attr:
            try:
                self.attr[attr] = self.attr[attr].pivot(self.event_n)
            except AttributeError:
                pass
        return self

    def shuffle(self):
        """ Shuffles the degree of a player. """
        # If using a play string for the degree
        #if self.synthdef == SamplePlayer and self.playstring is not None:
        #    # Shuffle the contents of playgroups among the whole string
        #    new_play_string = PlayString(self.playstring).shuffle()
        #    new_degree = Pattern(new_play_string).shuffle()
        #else:            
        #new_degree = self.attr['degree'].shuffle()
        new_degree = self.previous_patterns["degree"].root.shuffle()
        self._replace_degree(new_degree)
        return self


    def rotate(self, n=1):
        """ Rotates the values in the degree by 'n' """
        #self._replace_degree(self.attr['degree'].rotate(n))
        new_degree = self.previous_patterns["degree"].root.rotate(n)
        self._replace_degree(new_degree)
        return self

    def attrmap(self, key1, key2, mapping):
        """ Sets the attribute for self.key2 to self.key1
            altered with a mapping dictionary.
        """
        self.attr[key2] = self.attr[key1].map(mapping)
        return self

    def smap(self, kwargs):
        """ Like map but maps the degree to the sample attribute
        """
        self.attrmap("degree", "sample", kwargs)
        return self

    def map(self, other, mapping, otherattr="degree"):
        """ p1 >> pads().map(b1, {0: {oct=[4,5], dur=PDur(3,8), 2: oct})     """
        # Convert dict to {"oct": {4}}
        # key is the value of player key, attr is 
        for key, minimap in mapping.items():
            for attr, value in minimap.items():
                setattr(self, attr, mapvar(getattr(other, attr), values))
        return self

    
    # --- Misc. Standard Object methods

    def __int__(self):
        return int(self.now('degree'))

    def __float__(self):
        return float(self.now('degree'))

    def __add__(self, data):
        """ Change the degree modifier stream """
        self.mod_data = data
        if self.synthdef == SamplePlayer:
            # self.attr['sample'] = self.modifier + self.mod_data
            self.sample = self.modifier + self.mod_data
        else:
            #self.attr['degree'] = self.modifier + self.mod_data
            self.degree = self.modifier + self.mod_data
        return self

    def __sub__(self, data):
        """ Change the degree modifier stream """
        self.mod_data = 0 - data
        if self.synthdef == SamplePlayer:
            self.attr['sample'] = self.modifier + self.mod_data
        else:
            self.attr['degree'] = self.modifier + self.mod_data
        return self

    def __mul__(self, data):
        return self

    def __div__(self, data):
        return self

    # --- Data methods

    def __iter__(self):
        for _, value in self.event.items():
            yield value

    def number_of_layers(self, **kwargs):
        """ Returns the deepest nested item in the event """
        num = 1
        for attr, value in self.event.items():
            value = kwargs.get(attr, value)
            if isinstance(value, PGroup):
                l = pattern_depth(value)
            else:
                l = 1                
            if l >  num:
                num = l
        return num                

    def largest_attribute(self, **kwargs):
        """ Returns the length of the largest nested tuple in the current event dict """

        size = 1
        values = []

        for attr, value in self.event.items():
            value = kwargs.get(attr, value)
            l = get_expanded_len(value)
            if l > size:
                size = l
        return size

    def get_event_length(self, event=None, **kwargs):
        """ Returns the largest length value in the event dictionary """
        if event is None:
            
            event = self.event

        if kwargs:

            event = event.copy()
            event.update(kwargs)
        
        max_val = 0

        for attr, value in event.items():
            
            if isinstance(value, PGroup):
            
                l = len(value)
            
            else:
            
                l = 1

            if l > max_val:
                
                max_val = l

        return max_val

    def number_attr(self, attr):
        """ Returns true if the attribute should be a number """
        return not (self.synthdef == SamplePlayer and attr in ("degree", "freq"))

    def update_player_key(self, key, value, time):
        """  Forces object's dict uses PlayerKey instances
        """
        if (key not in self.__dict__) or (not isinstance(self.__dict__[key], PlayerKey)):

            self.__dict__[key] = PlayerKey(value, player=self, attr=key) 

        else:

            # Force values if not playing

            if self.isplaying is False:

                self.__dict__[key].set(value, time)

            else:

                self.__dict__[key].update(value, time)

        return

    def update_all_player_keys(self, ignore=[], event=None, **kwargs):
        """ Updates the internal values of player keys that have been accessed e.g. p1.pitch. If there is a delay,
            then schedule a function to update the values in the future. """

        # Don't bother if no keys are being accessed

        if len(self.accessed_keys) == 0:

            return

        if event is None:

            event = self.event

        delay = event.get("delay", 0)

        if isinstance(delay, PGroup):

            event_size = self.get_event_length(event, **kwargs)

            delays = itertools.cycle(delay)

            for i in range(event_size):

                delay = next(delays)

                # recursively unpack
                    
                new_event = {}

                for new_key, new_value in event.items():

                    if new_key in self.accessed_keys:

                        new_value = kwargs.get(new_key, new_value)

                        if isinstance(new_value, PGroup):

                            new_event[new_key]  = new_value[i]

                        else:

                            new_event[new_key] = new_value

                if isinstance(delay, PGroup):

                    # Recursively unpack and send messages

                    for i in range(self.get_event_length(new_event)):

                        self.update_all_player_keys(event=new_event, ignore=ignore, **kwargs)

                else:

                    self.update_player_key_from_event(new_event, time=self.event_index, ignore=ignore, delay=delay, **kwargs)

        else:

            self.update_player_key_from_event(event, time=self.event_index, ignore=ignore, delay=delay, **kwargs)

        return

    def update_player_key_from_event(self, event, time=None, delay=0, ignore=[], **kwargs):

        timestamp = self.event_index if time is None else time

        if delay == 0:

            for key in (x for x in self.accessed_keys if x not in ignore):

                self.update_player_key(key, kwargs.get(key, event.get(key, 0)), timestamp)

        else:

            func_args = (event, timestamp + delay, 0, ignore)

            self.metro.schedule(self.update_player_key_from_event, timestamp + delay, args=func_args, kwargs=kwargs)

        return

    def update_player_key_relation(self, item):
        """ Called during 'now' to update any Players that a player key is related to before using that value """

        # If this *is* the parent, just get the current value

        if item.parent is self:

            self.update_player_key(item.attr, self.now(item.attr), 0)

        # If the parent is in the same queue block, make sure its values are up-to-date

        elif self.queue_block is not None:

            # Try and find the item in the queue block

            try:

                queue_item = self.queue_block[item.player]

            except KeyError:

                queue_item = None

            # Update the parent with an up-to-date value

            if queue_item is not None and queue_item.called is False:
                    
                item.player.update_player_key(item.attr, item.player.now(item.attr), 0)

        return item.now()

    # --- Methods for preparing and sending OSC messages to SuperCollider

    def unpack(self, item):
        """ Converts a pgroup to floating point values and updates and time var or playerkey relations """

        if isinstance(item, GeneratorPattern):

            # "pop" value from the generator

            item = item.getitem() # could be renamed to "next"

        if isinstance(item, TimeVar):

            # Get current value if TimeVar

            item = item.now()

        if isinstance(item, NumberKey):

            # Update any relationships to the number key if necessary

            item = self.update_player_key_relation(item)

        if isinstance(item, PGroup):

            # Make sure any values in the PGroup have their "now" methods called

            item = item.convert_data(self.unpack)

        return item

    def get_key(self, key, i, **kwargs):
        return group_modi(kwargs.get(key, self.event[key]), i)

    # Private method

    def now(self, attr="degree", x=0, **kwargs):
        """ Calculates the values for each attr to send to the server at the current clock time """

        index = self.event_n + x

        try:

            if len(self.attr[attr]) > 0:

                attr_value = kwargs.get(attr, self.attr[attr][index])

            else:

                attr_value = 0 # maybe have a dict of defaults?

        # Debugging

        except KeyError as e:

            print(attr, self.attr[attr], index)
            raise(e)

        except ZeroDivisionError as e:

            print(self, attr, self.attr[attr], index)
            raise(e)

        # Force and timevar etc into floats

        if attr_value is not None and (not isinstance(attr_value, (int, float))):

            attr_value = self.unpack(attr_value)

        return attr_value

    def get_prime_funcs(self, event):
        """ Finds and PGroupPrimes in event and returns the modulated event dictionary """

        prime_keys = ("degree", "sample")

        # Go through priority keys

        for key in prime_keys:

            self.apply_prime_funcs(event, key)

        # Then do the rest (skipping prime)

        for key in event:

            if key not in prime_keys:

                self.apply_prime_funcs(event, key)

        return event

    @staticmethod
    def apply_prime_funcs(event, key):
        value = event[key]
        if isinstance(value, PGroup) and value.has_behaviour():
            func = value.get_behaviour()
            event = func(event, key)
        return event

    def unduplicate_durs(self, event):
        """ Converts values stored in event["dur"] in a tuple/PGroup into delays """

        # If there are more than one dur then add to the delay

        if "dur" in event:

            try:

                if len(event['dur']) > 1:

                    init_dur = event["dur"][0]

                    offset = PGroup(0|event['dur'][1:])

                    event["delay"] = event["delay"] + offset

                    event["dur"]   = float(init_dur)

                elif len(event['dur']) == 1:

                    event["dur"] = float(event["dur"][0])

            except TypeError:

                pass

        if "sus" in event:

            try:

                # Also update blur / sus

                if len(event['sus']) > 1:

                    min_sus = min(event['sus']) if min(event['sus']) else 1

                    offset = PGroup([(sus / min_sus) for sus in event["sus"]])

                    event["blur"] = event["blur"] * offset

                    event["sus"] = float(min_sus)

                elif len(event['sus']) == 1:

                    event["sus"] = float(event["sus"][0])

            except TypeError:

                pass

        return event

    def get_event(self):
        """ Returns a dictionary of attr -> now values """

        self.event = dict(map(lambda attr: (attr, self.now(attr)), self.attr.keys()))

        self.event = self.unduplicate_durs(self.event)

        self.event = self.get_prime_funcs(self.event)

        # Update internal player keys / schedule future updates

        self.update_all_player_keys()

        return self


    def send(self, timestamp=None, verbose=True, **kwargs):
        """ Goes through the  current event and compiles osc messages and sends to server via the tempo clock """

        timestamp = timestamp if timestamp is not None else self.queue_block.time

        # self.do_bang = False

        for i in range(self.get_event_length(**kwargs)):

            self.send_osc_message(self.event, i, timestamp=timestamp, verbose=verbose, **kwargs)

        # if self.do_bang:

        #     self.bang()

        return

    def send_osc_message(self, event, index, timestamp=None, verbose=True, **kwargs):
        """ Compiles and sends an individual OSC message created by recursively unpacking nested PGroups """

        packet = {}

        event=event.copy()
        event.update(kwargs)

        for key, value in event.items():

            # If we can index a value, trigger a new OSC message to send OSC messages for each

            # value = kwargs.get(key, value)

            if isinstance(value, PGroup):

                new_event = {}

                for new_key, new_value in event.items():

                    # new_value = kwargs.get(new_key, new_value)

                    if isinstance(new_value, PGroup):

                        new_event[new_key]  = new_value[index]

                    else:

                        new_event[new_key] = new_value

                # Recursively unpack and send messages

                for i in range(self.get_event_length(new_event)):

                    self.send_osc_message(new_event, i, timestamp, verbose)

                return

            else:

                # If it is a number, use the numbers (check for kwargs override)
                
                packet[key] = value

        # Special case modulations

        if ("amp" in packet) and ("amplify" in packet):

            packet["amp"] = packet["amp"] * packet["amplify"]

        # Send compiled messages

        self.push_osc_to_server(packet, timestamp, verbose, **kwargs)

        return

    def push_osc_to_server(self, packet, timestamp, verbose=True, **kwargs):
        """ Adds message head, calculating frequency then sends to server if verbose is True and 
            amp/bufnum values meet criteria """

        # Do any calculations e.g. frequency

        message = self.new_message_header(packet, **kwargs)

        # Only send if amp > 0 etc

        if verbose and (message["amp"] > 0) and ((self.synthdef != SamplePlayer and message["freq"] != None) or (self.synthdef == SamplePlayer and message["buf"] > 0)):

            # Need to send delay and synthdef separately

            delay = self.metro.beat_dur(message.get("delay", 0))

            synthdef = self.get_synth_name(message.get("buf", 0)) # to send to play1 or play2

            compiled_msg = self.metro.server.get_bundle(synthdef, message, timestamp = timestamp + delay)

            # We can set a condition to only send messages

            self.queue_block.append_osc_message(compiled_msg)

            # self.do_bang = True

        return

    def new_message_header(self, event, **kwargs):
        """ Returns the header of an osc message to be added to by osc_message() """

        # Let SC know the duration of 1 beat so effects can use it and adjust sustain too

        beat_dur = self.metro.beat_dur()

        message = {"beat_dur": beat_dur, "sus": kwargs.get("sus", event["sus"]) * beat_dur}

        if self.synthdef == SamplePlayer:

            degree = kwargs.get("degree", event['degree'])
            sample = kwargs.get("sample", event["sample"])
            rate   = kwargs.get("rate", event["rate"])

            if rate < 0:

                sus = kwargs.get("sus", event["sus"])

                pos = self.metro.beat_dur(sus)

            else:

                pos = 0 
 
            buf  = self.samples.getBufferFromSymbol(str(degree), sample).bufnum
            
            message.update( {'buf': buf,'pos': pos} )

            # Update player key

            if "buf" in self.accessed_keys:

                self.buf = buf

        elif self.synthdef == LoopPlayer:

            pos = kwargs.get("degree", event["degree"])
            buf = kwargs.get("buf", event["buf"])

            # Get a user-specified tempo

            given_tempo = kwargs.get("tempo", self.event.get("tempo", self.metro.bpm))

            if given_tempo in (None, 0):

                tempo = 1

            else:

                tempo = self.metro.bpm / given_tempo

            # Set the position in "beats"

            pos = pos * tempo * self.metro.beat_dur(1)

            # If there is a negative rate, move the pos forward

            rate = kwargs.get("rate", event["rate"])

            if rate == 0:

                rate = 1

            # Adjust the rate to a given tempo

            rate = float(tempo * rate)

            if rate < 0:

                sus = kwargs.get("sus", event["sus"])

                pos += self.metro.beat_dur(sus)

            message.update( {'pos': pos, 'buf': buf, 'rate': rate} )

        else:

            degree = kwargs.get("degree", event["degree"])
            octave = kwargs.get("oct", event["oct"])
            root   = kwargs.get("root", event["root"])

            scale  = kwargs.get("scale", self.scale)

            if degree == None:

                freq, midinote = None, None

            else:

                freq, midinote = get_freq_and_midi(degree, octave, root, scale)
                
            message.update({'freq':  freq, 'midinote': midinote})

            # Updater player key

            if "freq" in self.accessed_keys:

                self.freq = freq

            if "midinote" in self.accessed_keys:
    
               self.midinote = midinote

        # Update the dict with other values from the event

        event.update(message)

        # Remove keys we dont need

        del event["bpm"]
            
        return event        

    def set_queue_block(self, queue_block):
        """ Gives this player object a reference to the other items that are 
            scheduled at the same time """
        self.queue_block = queue_block
        return

    def get_synth_name(self, buf=0):
        """ Returns the real SynthDef name of the player. Useful only for "play" 
            as there is a play1 and play2 SynthDef for playing audio files with
            one or two channels respectively. """
        if self.synthdef == SamplePlayer:
            numChannels = self.samples.getBuffer(buf).channels
            if numChannels == 1:
                synthdef = "play1"
            else:
                synthdef = "play2"
        else:
            synthdef = str(self.synthdef)
        return synthdef

    def addfx(self, **kwargs):
        """ Not implemented - add an effect to the SynthDef bus on SuperCollider
            after it has been triggered. """
        return self

    #: Methods for stop/starting players

    def kill(self):
        """ Removes this object from the Clock and resets itself"""
        
        self.isplaying = False
        self.stopping = True
        
        self.reset()

        if self in self.metro.playing:
        
            self.metro.playing.remove(self)
        
        return
        
    def stop(self, N=0):
        
        """ Removes the player from the Tempo clock and changes its internal
            playing state to False in N bars time
            - When N is 0 it stops immediately"""

        self.stopping = True        
        self.stop_point = self.metro.now()

        if N > 0:

            self.stop_point = self.metro.next_bar() + ((N-1) * self.metro.bar_length())

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

    # Methods for collaborative performance
    #
    # e.g. follow
    #

    def accompany(self, other, values=[0,2,4], debug=False):
        """ Similar to "follow" but when the value has changed """

        if isinstance(other, self.__class__):

            self.degree = other.degree.accompany()
        
        return self

    def follow(self, other=False):
        """ Takes a Player object and then follows the notes """

        if isinstance(other, self.__class__):

            self.degree = other.degree

        return self

    def versus(self, other_key, rule=lambda x, y: x > y, attr=None):
        """ Sets the 'amplify' key for both players to be dependent on the comparison of keys """

        # Get reference to the second player object

        other = other_key.player

        # Get the attribute from the key to versus

        this_key = getattr(self, other_key.attr if attr is None else attr)

        # Set amplifications based on the rule

        self.amplify  = this_key.transform(lambda value: rule(value, other_key.now()))
        other.amplify = this_key.transform(lambda value: not rule(value, other_key.now()))

        return self

    def reload(self):
        """ If this is a 'play' or 'loop' SynthDef, reload the filename used"""

        if self.synthdef == LoopPlayer:

            Samples.reload(self.filename)

        return self

    def only(self):
        """ Stops all players except this one """
        for player in list(self.metro.playing):
            if player is not self:
                player.stop()
        return self

    def solo(self, action=1):
        """ Silences all players except this player. Undo the solo
            by using `Player.solo(0)` """

        action=int(action)

        if action == 0:

            self.metro.solo.reset()

        elif action == 1:

            self.metro.solo.set(self)

        elif action == 2:

            pass

        return self

    def versus_old(self, other, key = lambda x: x.freq, f=max):
        """ Takes another Player object and a function that takes
            two player arguments and returns one, default is the higher
            pitched
        """
        if other is not None:
            assert(other.__class__ == self.__class__) # make sure it's using another player
            func = lambda x, y: f(x, y, key=key)
            self.condition  = lambda: func(self, other) == self
            other.condition = lambda: func(self, other) == other
            self._versus = other
        else:
            self.condition  = lambda: True
            self._versus.condition = lambda: True
            self._versus = None
        return self

    # def versus(self, other, func = lambda a, b: a > b):

    #     self.amp  = self.pitch > other.pitch
    #     other.amp = other.pitch > self.pitch

    #     return self
    

    # Utils

    def num_key_references(self):
        """ Returns the number of 'references' for the
            attr which references the most other players """
        num = 0
        for attr in self.attr.values():
            if isinstance(attr, PlayerKey):
                if attr.num_ref > num:
                    num = attr.num_ref
        return num

    def _replace_degree(self, new_degree):
        # Update the GUI if possible
        #if self.widget:
        #    if self.synthdef == SamplePlayer:
        #        if self.playstring is not None:
        #            # Replace old_string with new string (only works with plain string patterns)
        #            new_string = new_degree.string()
        #            self.widget.addTask(target=self.widget.replace, args=(self.line_number, self.playstring, new_string))
        #            self.playstring = new_string
        #    else:
        #        # Replaces the degree pattern in the widget (experimental)
        #        # self.widget.addTask(target=self.widget.replace_re, args=(self.line_number,), kwargs={'new':str(new_degree)})
        #        self.playstring = str(new_degree)
        setattr(self, 'degree', new_degree)
        return

    def multiply(self, n=2):
        self.attr['degree'] = self.attr['degree'] * n
        return self

    def degrade(self, amount=0.5):
        """ Sets the amp modifier to a random array of 0s and 1s
            amount=0.5 weights the array to equal numbers """
        if float(amount) <= 0:
            self.amplify = 1
        else:
            self.amplify = PwRand([0, self.attr["amplify"]],[int(amount*10), max(10 - int(amount),0)])
        return self

    def changeSynth(self, list_of_synthdefs):
        new_synth = choice(list_of_synthdefs)
        if isinstance(new_synth, SynthDef):
            new_synth = str(new_synth.name)
        self.synthdef = new_synth
        return self

    """

        Modifier Methods
        ----------------

        Other modifiers for affecting the playback of Players

    """

    def offbeat(self, dur=1):
        """ Off sets the next event occurence """

        self.dur = abs(dur)
        self.delay = abs(dur) / 2

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
        if self.id is not None:
            return "<{} - {}>".format(self.id, self.synthdef)
        else:
            return "a '{}' Player Object".format(self.synthdef)

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
        

###### GROUP OBJECT

class Group:

    metro = None

    def __init__(self, *args):

        self.players = list(args)

    def add(self, other):
        self.players.append(other)

    def __len__(self):
        return len(self.players)

    def __str__(self):
        return str(self.players)

    def solo(self, arg=True):

        if self.metro is None:

            self.__class__.metro = Player.metro

        if arg:
            
            self.metro.solo.set(self.players[0])

            for player in self.players[1:]:

                self.metro.solo.add(player)

        else:

            self.metro.solo.reset()

        return self
        
    def only(self):

        if self.metro is None:

            self.__class__.metro = Player.metro
        
        for player in list(self.metro.playing):
            
            if player not in self.players:
                
                player.stop()

        return self

    def iterate(self, dur=4):
        if dur == 0 or dur is None:
            self.amplify=1
        else:
            delay, on = 0, float(dur) / len(self.players)
            for player in self.players:
                player.amplify=TimeVar([0,1,0],[delay, on, dur-delay])
                delay += on
        return           

    def __setattr__(self, name, value):
        try:
            for p in self.players:
                try:
                    setattr(p, name, value)
                except:
                    WarningMsg("'%s' object has no attribute '%s'" % (str(p), name))
        except KeyError :
            self.__dict__[name] = value 
        return self        

    def __getattr__(self, name):
        """ Returns a Pattern object containing the desired attribute for each player in the group  """
        if name == "players":
            return self.__dict__["players"]
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
        self.dur = dur if not isinstance(dur, self.__class__) else dur.dur
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
    def __eq__(self, other):
        return (self.dur == other)
    def __ne__(self, other):
        return (self.dur != other)
    def __lt__(self, other):
        return (self.dur < other)
    def __le__(self, other):
        return (self.dur <= other)
    def __gt__(self, other):
        return (self.dur > other)
    def __ge__(self, other):
        return (self.dur >= other)
    def __int__(self):
        return int(self.dur)
    def __float__(self):
        return float(self.dur)

class PlayerKeyException(Exception):
    pass
