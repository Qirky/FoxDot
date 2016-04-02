"""

    Copyright Ryan Kirkbride 2015

    This is the module that combines all the other modules as if it were the live
    environment. The main.py application execute() method sends the string over to
    this module, which is analysed and sent back as the raw python code to execute.

    This module also handles the time keeping aspect. There is a constant tempo
    clock running that has a queue and plays the items accordingly

    Note: The code below IS executed in the Environment and can be accessed by the user!

"""
from re import match
from random import choice as choose

from TempoClock import *
from ServerManager import *
from Players import *
from Patterns import *
from Code import *
from TimeVar import *
import Scale

# Default server connection and metronome
        
Server = ServerManager()

Clock = TempoClock()

BufferManager = BufferManager(Server) # From Players NOT Buffers
BufferManager.sendToServer()

# Clock dependant variable - stream / inherit float / allow float/int methods and change code

class var(TimeVar):

    def __init__(self, values=[0], dur=4):

        TimeVar.__init__(self, values, dur, Clock)

Var = var # Allow caps

# FoxDot Class that is used to return types of players easily

class Player(synth_):
    
    def __init__(self, SynthDef, degree=[0], **kwargs):
        synth_.__init__(self, SynthDef, degree)
        # Set defaults
        self.metro = Clock
        self.server = Server
        self.scale = kwargs.get( "scale", Scale.default() )
        self.dur = self.attr['dur'] = 1
        self.sus = self.attr['sus'] = 1
        # Add to clock and update with keyword arguments
        self.begin()
        self.update(SynthDef, degree, **kwargs)
        
class SamplePlayer(samples_):

    def __init__(self, string, **kwargs):
        samples_.__init__(self, ''.join(Place(string)), **kwargs)
        # Set defaults
        self.metro = Clock
        self.server = Server
        self.dur = self.attr['dur'] = self.dur_val = self.attr['dur_val'] = 0.5
        # Add to clock and update
        self.begin()
        self.update(self.degree)

# Misc. Functions

def Ramp(start=0, end=1, dur=8, step=0.25):
    size = dur/float(step)
    return var([start + end * n/size for n in range(int(size))], step)

def iRamp(start=0, end=1, dur=8, step=0.25):
    size = dur/float(step)
    return var([start + end * n/size for n in range(int(size))] + [end], [step]*int(size)+[inf])
