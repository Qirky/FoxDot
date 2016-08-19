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
import Scale
import Root

""" SCLang """

import SCLang
from SCLang import SynthDefs, Env
from SCLang.SynthDefs import *


""" CLOCK """

Clock = TempoClock()
when.metro = var.metro = Clock
PlayerObject.metro  = Clock
PlayerObject.server = Server
PlayerObject.default_scale = Scale.default()
PlayerObject.default_root  = Root.default()

BufferManager.server = Server
BufferManager.load()

FoxDotCode.namespace=globals()

""" Preset PlayerObjects """

alphabet = 'abcdefghijklmnopqrstuvwxyz'
numbers  = '0123456789'

# 1 Letter Player Objects

for char in alphabet:

    FoxDotCode.namespace[char] = PlayerObject(char)

# 2 Letter Player Objects

for char1 in alphabet:

    for char2 in alphabet + numbers:

        name = char1+char2

        FoxDotCode.namespace[name] = PlayerObject(name)


""" IDE """

def start():

    from Interface import FoxDot
    
    try:
        
        FoxDot().run()
        
    except KeyboardInterrupt, SystemExit:

        Clock.stop()
        Server.quit()
