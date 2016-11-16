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
import Scale
import Root

""" SCLang """

from SCLang import Synths, Env
from SCLang.SynthDefs import *

""" CLOCK """

Clock = TempoClock()
Clock.when_statements = when

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

alphabet = 'abcdefghijklmnopqrstuvwxyz'
numbers  = '0123456789'

# 1 Letter Player Objects

for char in alphabet:

    FoxDotCode.namespace[char] = Player()

# 2 Letter Player Objects

for char1 in alphabet:

    for char2 in alphabet + numbers:

        name = char1+char2

        FoxDotCode.namespace[name] = Player()

# misc

class futureprint:
    """ Wraps Python 2.7 print statements as a function """
    def __init__(self, string=""):
        self.string = string
    def __call__(self):
        print self.string

PatternTypes = []
for pattern_name in sorted(classes(Sequences)):
    if len(PatternTypes) == 0:
        PatternTypes.append(pattern_name)
    else:
        if pattern_name.upper() !=  PatternTypes[-1].upper():
            PatternTypes.append(pattern_name)
        



""" IDE """
from Workspace import workspace

# Share the GUI information with the user

workspace.namespace=FoxDotCode.namespace

FoxDot = workspace()

def start():
    
    try:
             
        FoxDot.run()
        
    except (KeyboardInterrupt, SystemExit):

        Clock.stop()
        Server.quit()
