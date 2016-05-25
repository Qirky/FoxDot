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

"""
    These define 'global' defaults:

        - Tempo Clock

        - Server Connection

        - Sample Buffers

"""
##############
""" SERVER """

# Connect to server
        
Server = ServerManager()

# Set the SCLang interpreter server

SCLang.SynthDef.server = SCLangManager()

# Import existing SynthDefs

import SuperCollider.SynthDefs as SynthDefs

# Set up the SuperCollider Buffers

Buffers = BufferManager(Server)
Buffers.load()


""" CLOCK """

Clock = TempoClock()

"""
    Below are the classes for the three main aspects of FoxDot:

        - Player Objects

        - Sample Player Objects

        - Time-Dependant Variables        

"""


class Player(SYNTH_PLAYER):

    def __init__(self, SynthDef, degree=[0], **kwargs):

        SYNTH_PLAYER.__init__(self, SynthDef, degree)

        # Set defaults
        
        self.metro = Clock
        self.server = Server
        self.scale = kwargs.get( "scale", Scale.default() )
        self.root = self.attr['root']  = kwargs.get( "root",  Root.default() )
        self.dur = self.attr['dur'] = 1
        self.sus = self.attr['sus'] = 1

        # Finish init (any assigned attributes not go in the Player.attr dict
        
        self._INIT = True

        # Update attributes
        
        self.update(SynthDef, degree, **kwargs)
        
        # Add to clock and update with keyword arguments
        
        self.isplaying = True
        self.event_index = self.metro.NextBar()
        self.event_n = 0
        self.metro.Schedule(self, self.event_index)

        
        
class SamplePlayer(SAMPLE_PLAYER):

    def __init__(self, string, **kwargs):
        
        SAMPLE_PLAYER.__init__(self, string, **kwargs)
        
        # Set defaults
        self.metro   = Clock
        self.server  = Server
        self.dur     = self.attr['dur']     = 0.5
        self.dur_val = self.attr['dur_val'] = 0.5

        # Finish init

        self._INIT = True

        # Update attributes
        
        self.update(self.degree)

        # Add to clock and update

        self.isplaying = True
        self.event_index = self.metro.NextBar()
        self.metro.Schedule(self, self.event_index)

class Var(TimeVar):

    """

        Time-Dependant Variable Class
        =============================

        Var(Values, Durations) -> TimeVar

        Creates a time-dependant variable that uses the default clock implicitly.
        Durations has a value of 4 by default and can be a single number or list
        of ints or floats.
        

    """

    def __init__(self, values=[0], dur=4):

        TimeVar.__init__(self, values, dur, Clock)

var = Var
