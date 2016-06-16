"""

    Copyright Ryan Kirkbride 2015

"""
from random import choice as choose

from TempoClock import *
from ServerManager import *
from Players import *
from Patterns import *
from Code import *
from TimeVar import *
from SuperCollider import *
import Scale
import Root

""" SERVER """
     
Server = ServerManager()

""" CLOCK """

Clock = TempoClock()

Var.metro = Clock
PlayerObject.metro, PlayerObject.server = Clock, Server
Player.default_scale = Scale.default()
Player.default_root  = Root.default()
FoxCode.namespace=globals()

""" IDE """

def start():
    from Interface import FoxDot
    FoxDot().run()
