"""

    Copyright Ryan Kirkbride 2015

"""

""" SERVER """

from ServerManager import Server

""" IMPORTS """

from random import choice as choose

from TempoClock import *
from Players import *
from Patterns import *
from Code import *
from TimeVar import *
from SuperCollider.SCLang import SynthDefs

import SuperCollider.SynthDefs
import Scale
import Root

""" CLOCK """

Clock = TempoClock()
Var.metro = Clock
PlayerObject.metro, PlayerObject.server = Clock, Server
Player.default_scale = Scale.default()
Player.default_root  = Root.default()
FoxCode.namespace=globals()

""" IDE """

def start(*args):

    from Interface import FoxDot
    
    try:

        if "-boot" in args:

            Server.boot()
            BufferManager.load()
        
        FoxDot().run()
        
    except KeyboardInterrupt, SystemExit:

        Clock.stop()
        Server.quit()
