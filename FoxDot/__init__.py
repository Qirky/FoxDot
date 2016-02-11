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

# Define default variables - these are used in Code.new_player() DO NOT CHANGE
        
Server = ServerManager()

Clock = TempoClock()

DefaultScale = Scale.Scale("major")

# Clock dependant variable - stream / inherit float / allow float/int methods and change code

class var(TimeVar):

    def __init__(self, values, dur=4):

        TimeVar.__init__(self, values, dur, Clock)

Var = var # Allow caps

# FoxDot Class that is used to return types of players easily

class Player(new_):
    
    CREATED = False

    def __init__(self, SynthDef, degree=[0], **kwargs):
        new_.__init__(self, SynthDef, degree, **kwargs)
        self.metro = Clock
        self.server = Server
        self.scale = kwargs.get("scale", DefaultScale)
        self.begin()
        self.CREATED = True

    def begin(self):
        self.metro.playing.append(self)
        self.update_clock()
        return

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if self.CREATED and type(value) != str:
            self.attr[name] = value
        return


class SamplePlayer(samples_):

    CREATED = False

    def __init__(self, string, **kwargs):
        samples_.__init__(self, ''.join(Place(string)), **kwargs)
        self.metro = Clock
        self.server = Server
        self.begin()
        self.CREATED = True

    def begin(self):
        self.metro.playing.append(self)
        self.update_clock()
        return

# Misc. Functions

def Ramp(start=0, end=1, t=8):
    """ Returns a timevar that increase from start to end in time t then back to start """
    step = 0.25
    size = t / step
    dur = [step] * int(size) + [inf]
    val = irange(start, end, (end-start)/size)[:int(size)] + [start]
    return var(val, dur)

class SuperColliderSynthDefs:

    with open('startup.scd') as f:
        sc = f.readlines()    
    patt = r'SynthDef.*?\\(.*?)'

    names = [match(patt, line).group(1) for line in sc if "SynthDef" in line and not line.startswith("/")]

    def __init__(self):
        pass
    def __str__(self):
        return str(self.names)
    def __repr__(self):
        return str(self.names)
    def __len__(self):
        return len(self.names)
    def __iter__(self):
        for x in self.names:
            yield x
    def __getitem__(self, key):
        return self.names[key]
    def __setitem__(self, name, value):
        raise AttributeError("SynthDefs cannot be altered using FoxDot code")
    def __call__(self):
        return self.names
    def choose(self):
        return choose(self.names)

SynthDefs = SuperColliderSynthDefs() 
