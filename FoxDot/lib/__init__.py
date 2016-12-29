"""

    Copyright Ryan Kirkbride 2015

"""

""" CODE EXEC MODULE """

from Code import *

""" SERVER """

from ServerManager import Server

""" IMPORTS """

from random import choice as choose

from TempoClock import *
from Players import *
from Patterns import *
from TimeVar import *
from Constants import *
from Midi import *
import Scale
import Root

""" SCLang """

from SCLang import Synths, Env
from SCLang.SynthDefs import *

""" CLOCK """

Clock = TempoClock()
# Clock.when_statements = when

when.metro = var.metro = Clock

Player.metro  = Clock
Player.server = Server
Player.default_scale = Scale.default()
Player.default_root  = Root.default()

Clock.start()

BufferManager.server = Server
BufferManager.load()

FoxDotCode.namespace=globals()

""" Preset PlayerObjects """

alphabet = list('abcdefghijklmnopqrstuvwxyz')
numbers  = list('0123456789') + [""]

for char1 in alphabet:

    for char2 in alphabet + numbers:

        FoxDotCode.namespace[char1 + char2] = Player()

""" List of Patterns """

PatternTypes = []
for pattern_name in sorted(classes(Sequences)):
    if len(PatternTypes) == 0:
        PatternTypes.append(pattern_name)
    else:
        if pattern_name.upper() !=  PatternTypes[-1].upper():
            PatternTypes.append(pattern_name)
        
