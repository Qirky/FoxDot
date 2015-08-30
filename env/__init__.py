"""

This is the module that combines all the other modules as if it were the live
environment. The main.py application execute() method sends the string over to
this module, which is analysed and sent back as the raw python code to execute.

This module also handles the time keeping aspect. There is a constant tempo
clock running that has a queue and plays the items accordingly

"""

### Note: The code below IS executed in the Environment and can be accessed by the user!

import foxdot
from TempoClock import *
from ServerManager import *
from instruments import *

import Scale

# Python stlib

from random import choice as choose
import random


# --------------------- Handling Clock
        
server_ = ServerManager()

clock_ = TempoClock()

# Define global variables

default_scale = Scale.Scale("major")

# Define python functions that can be used in the live code

# Shuffling lists / create shuffled lists etc

from instruments import Place
from instruments import stutter_stream as Stutter

def Shuf(a, b=None, size=None):

    if type(a) == list:

        random.shuffle(a)

        return a

    try:
        if not size:
            size = b - a
    except:
        if not size:
            size = a
            
    return [random.randrange(a, b) for i in range(size)]


def fShuf(a, b=None, size=8):

    if b:

        L = [a + (n * ( (b-a) / float(size))) for n in range(size)]

    else:

        L = [n * ( a / float(size)) for n in range(size)]

    random.shuffle(L)

    return L

def White(lo=0, hi=1, mode=None, size=256):

    lo = float(lo)
    hi = float(hi)

    if not mode or lo > mode or mode > hi:

        mode = (lo + hi) / 2.0

    L = [random.triangular(lo, hi, mode) for n in range(size)]

    return L


def Walk(hi=8, variation=1, size=256):

    stream = [0]

    variation = 1.0 / variation

    step = random.choice([1,-1])

    while len(stream) < size:

        step = step * (-1)

        for x in range( int(hi * random.triangular(variation, 1)) - 1 ):

            stream.append( stream[-1] + step )

            if len(stream) == size:
                break

    return stream


def Sparse(arr=[0,1], hi=8):

    stream =[]

    return strema


def Geom(n, lo=1, hi=None):

    if not hi:

        hi = max(lo, 1)
        lo = min(lo, 1)

    return [n**i for i in range(lo, hi+1)]


def Rand(a, b=None, size=256):

    if type(a) == list:

        return [random.choice(a) for n in range(size)]

    else:

        return [random.randrange(a, b) for n in range(size)]

def Rint(a, b=None):

    if b:

        return random.randrange(a, b)

    else:

        return random.randrange(0, a)



def Sine(size=16):

    a = [-1.0 + (2*n)/float(size / 2) for n in range(size)]
    b = [ 1.0 - (2*n)/float(size / 2) for n in range(size)]

    return a + b


def Rhythm(string, step=0.5):

    stream = []

    dur = 0.0

    in_br = False

    for i, char in enumerate(string):

       # Needs work 

        if char == "[":

            in_br = True

            dur -= step

        elif char == "]":

            in_br = False

            dur -= step
        
        elif char != " ":

            stream.append(dur)

            dur = 0.0

        elif i == len(string) - 1:

            stream.append(dur + step)


        if in_br:

            dur += step/2.0

        else:   
    
            dur += step

    return stream[1:]

            

        


    

