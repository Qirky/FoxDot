"""

FoxDot is a Python library and programming environment that provides a fast and 
user-friendly abstraction to the powerful audio-engine, SuperCollider. It comes 
with its own IDE, which means it can be used straight out of the box; all you need 
is Python and SuperCollider and you're ready to go!

For more information on installation, check out [the guide](http://foxdot.org/installation), 
or if you're already set up, you can also find a useful starter guide that introduces the
key components of FoxDot on [the website](http://foxdot.org/).

Please see the documentation for more detailed information on the FoxDot classes 
and how to implement them.

Copyright Ryan Kirkbride 2015
"""

from __future__ import absolute_import, division, print_function

__version__ = "0.6.2"

import logging

from .Code import *

FoxDotCode.namespace = globals()

from .TempoClock import *
from .Buffers import *
from .Players import *
from .Patterns import *
from .Effects import *
from .TimeVar import *
from .Constants import *
from .Midi import *
from .Settings import *
from .SCLang._SynthDefs import *
from .ServerManager import *
from .SCLang import SynthDefs, Env, SynthDef, CompiledSynthDef
from .Root import Root
from .Scale import Scale, Tuning
from .Workspace import get_keywords

# stdlib imports

from random import choice as choose

# Define any custom functions
    
@PatternMethod
def __getitem__(self, key):
    """ Overrides the Pattern.__getitem__ to allow indexing
        by TimeVar and PlayerKey instances. """
    if isinstance(key, PlayerKey):
        # Create a player key whose calculation is get_item
        return key.index(self)
    elif isinstance(key, TimeVar):
        # Create a TimeVar of a PGroup that can then be indexed by the key
        item = TimeVar(tuple(self.data))
        item.dependency = key
        item.evaluate = fetch(Get)
        return item
    else:
        return self.getitem(key)

def player_method(f):
    """ Decorator for assigning functions as Player methods. 

    >>> @player_method
    ... def test(self):
    ...    print(self.degree)

    >>> p1.test()
    """
    setattr(Player, f.__name__, f)
    return getattr(Player, f.__name__)

PlayerMethod = player_method # Temporary alias

def _futureBarDecorator(n, multiplier=1):
    if callable(n):
        Clock.schedule(n, Clock.next_bar())
        return n
    def wrapper(f):
        Clock.schedule(f, Clock.next_bar() + (n * multiplier))
        return f
    return wrapper

def next_bar(n=0):
    ''' Schedule functions when you define them with @nextBar
    Functions will run n beats into the next bar.

    >>> nextBar(v1.solo)
    or
    >>> @nextBar
    ... def dostuff():
    ...     v1.solo()
    '''
    return _futureBarDecorator(n)

nextBar = next_bar # temporary alias

def futureBar(n=0):
    ''' Schedule functions when you define them with @futureBar
    Functions will run n bars in the future (0 is the next bar)

    >>> futureBar(v1.solo)
    or
    >>> @futureBar(4)
    ... def dostuff():
    ...     v1.solo()
    '''
    return _futureBarDecorator(n, Clock.bar_length())

def update_foxdot_clock(clock):
    """ Tells the TimeVar, Player, and MidiIn classes to use 
        a new instance of TempoClock. """

    assert isinstance(clock, TempoClock)

    for item in (TimeVar, Player, MidiIn):

        item.set_clock(clock)

def update_foxdot_server(serv):
    """ Tells the `Effect` and`TempoClock`classes to send OSC messages to
        a new ServerManager instance.
    """

    assert isinstance(serv, ServerManager)

    TempoClock.set_server(serv)
    SynthDefs.set_server(serv)

    return

def instantiate_player_objects():
    """ Instantiates all two-character variable Player Objects """
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    numbers  = list('0123456789')

    for char1 in alphabet:

        group = []

        for char2 in alphabet + numbers:

            arg = char1 + char2

            FoxDotCode.namespace[arg] = EmptyPlayer(arg)

            group.append(arg)

        FoxDotCode.namespace[char1 + "_all"] = Group(*[FoxDotCode.namespace[char1+str(n)] for n in range(10)])

    return

def Master():
    """ Returns a `Group` containing all the players currently active in the Clock """
    return Group(*Clock.playing)

def Ramp(t=32, ramp_time=4):
    """ Returns a `linvar` that goes from 0 to 1 over the course of the last
        `ramp_time` bars of every `t` length cycle. """
    return linvar([0,0,1,0],[t-ramp_time, ramp_time, 0, 0])

def allow_connections(valid = True, *args, **kwargs):
    """ Starts a new instance of ServerManager.TempoServer and connects it with the clock. Default port is 57999 """
    if valid:
        Clock.start_tempo_server(TempoServer, **kwargs)
        print("Listening for connections on {}".format(Clock.tempo_server))
    else:
        Clock.kill_tempo_server()
        print("Closed connections")
    return

# Create a clock and define functions

logging.basicConfig(level=logging.ERROR)
when.set_namespace(FoxDotCode) # experimental

Clock = TempoClock()
update_foxdot_server(DefaultServer)
update_foxdot_clock(Clock)
instantiate_player_objects()
