"""

    Copyright Ryan Kirkbride 2015

    This is the module that combines all the other modules as if it were the live
    environment. The main.py application execute() method sends the string over to
    this module, which is analysed and sent back as the raw python code to execute.

    This module also handles the time keeping aspect. There is a constant tempo
    clock running that has a queue and plays the items accordingly

    Note: The code below IS executed in the Environment and can be accessed by the user!

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
