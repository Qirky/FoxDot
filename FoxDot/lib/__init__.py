"""

    Copyright Ryan Kirkbride 2015

"""

from Code import *
from Code import __when__

FoxDotCode.namespace = globals()

from TempoClock import *
from Players import *
from Patterns import *
from Effects import *
from TimeVar import *
from Constants import *
from Midi import *
from Settings import *
from SCLang.Definitions import *
from SCLang import SynthDefs, Env, SynthDef
from ServerManager import Server
import Scale
import Root

# stdlib imports

from random import choice as choose

# Create a clock and define functions

Clock = TempoClock()

# Give the server information about Effects

Server.setFx(FxList)

# Define any custom functions

def nextBar(f, n=0):
    ''' Schedule functions when you define them with @nextBar'''
    Clock.schedule(f, Clock.next_bar() + n)
    return f

# Assign the clock to time-keeping classes

var.metro     = Clock
Player.metro  = Clock

# Players and effects need reference to SC server

Player.server = Server
Effect.server = Server

# Create preset Players

alphabet = list('abcdefghijklmnopqrstuvwxyz')
numbers  = list('0123456789') + [""]

for char1 in alphabet:

    for char2 in alphabet + numbers:

        FoxDotCode.namespace[char1 + char2] = Player()

# Keep a list of pattern names

PatternTypes = []
for pattern_name in sorted(classes(Sequences)):
    if len(PatternTypes) == 0:
        PatternTypes.append(pattern_name)
    else:
        if pattern_name.upper() !=  PatternTypes[-1].upper():
            PatternTypes.append(pattern_name)

# Give the __when__ statement access to the  global namespace

__when__.set_namespace(FoxDotCode)

# Start the TempoClock

Clock.start()
