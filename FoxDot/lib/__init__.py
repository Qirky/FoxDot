"""

    Copyright Ryan Kirkbride 2015

"""

from __future__ import absolute_import, division, print_function

from .Code import *
from .Code import __when__

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
from .SCLang import SynthDefs, Env, SynthDef
from .ServerManager import Server
from .Root import Root
from .Scale import Scale
from .Workspace import get_keywords

# stdlib imports

from random import choice as choose

# Create a clock and define functions

Clock = TempoClock()

# Give Players a reference to the Sample Library

Player.samples = Samples

# Give the server information about Effects

Server.setFx(FxList)

# Define any custom functions

def nextBar(n=0):
    ''' Schedule functions when you define them with @nextBar'''
    if callable(n):
        Clock.schedule(n, Clock.next_bar())
        return n
    def wrapper(f):
        Clock.schedule(f, Clock.next_bar() + n)
        return f
    return wrapper

# Assign the clock to time-keeping classes

for item in (TimeVar, Player, Server, MidiIn):

    item.metro = Clock

# Players and effects etc need reference to SC server

for item in (Player, Effect, QueueItem, Clock):

    item.server = Server

# Create preset Players

alphabet = list('abcdefghijklmnopqrstuvwxyz')
numbers  = list('0123456789') + [""]

for char1 in alphabet:

    group = []

    for char2 in alphabet + numbers:

        arg = char1 + char2

        FoxDotCode.namespace[arg] = Player()

        group.append(arg)

    FoxDotCode.namespace[char1 + "_"] = Group(*[FoxDotCode.namespace[char1+str(n)] for n in range(10)])

# Create an empty item

FoxDotCode.namespace["_"] = EmptyItem()

# Give the __when__ statement access to the  global namespace

__when__.set_namespace(FoxDotCode)
