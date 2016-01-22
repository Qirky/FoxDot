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

from TempoClock import *
from ServerManager import *
from Players import *
from Patterns import *
from Code import *
import Scale

# Trailing underscore indicates a variable that is not necessarily intended for use
        
server_ = ServerManager()

# Define default variables - these are used in Code.new_player() DO NOT CHANGE

Clock = TempoClock()

default_scale = Scale.Scale("major")

# Clock dependant variable - stream / inherit float / allow float/int methods and change code

class var:

    def __init__(self, values, dur=4):

        # Initiate values and clock

        self.metro  = Clock
        self.seq    = values
        self.values = None
        self.dur    = dur

        self.update(values, dur)

        return

    def __str__(self):

        a = [str(i) for i in self.seq]
        b = [str(i) for i in self.dur]

        return "var([%s],[%s]) -> %s" % (",".join(a), ",".join(b), str(self.now()))

    def length(self):

        return sum(self.dur)

    def __len__(self):

        try:

            return len(self.now())

        except:

            return 1

    def __int__(self):

        return int(self.now())

    def __add__(self, n):

        return var([val+n for val in self.seq], self.dur)

    def __sub__(self, n):

        return var([val-n for val in self.seq], self.dur)

    def __float__(self):

        return float(self.now())

    def __eq__(self, other):

        return other == TimeVar

    def __ne__(self, other):

        return other != TimeVar

    def __iter__(self):

        try:

            for x in self.now():

                yield x

        except:

            yield self.now()

    def update(self, values, dur=None):

        """ Changes the values for any player using this var """

        if dur:

            self.dur = asStream(dur)

        # Update seq values

        self.seq = asStream(values)

        dur = self.dur
        values = self.seq

        lv = len(values)
        ld = len(dur)

        stream = []

        for i in range(max(lv, ld)):
            stream += [values[i % lv]]*int((dur[i % ld]*self.metro.steps))

        self.values = stream

        return
    
    def now(self):
        """ Returns the value at the current clock time """

        i = self.metro.now() % len(self.values)

        return self.values[i]

    def durs(self):

        return self.dur

    def vals(self):

        return self.seq

Var = var # Can be capitalised or not

patt = r'SynthDef.*?\\(.*?),'

def SynthDefs():
    """ Returns a list of all the available SynthDefs in startup.scd """
    f = open('startup.scd')
    sc = f.readlines()    
    f.close()
    return [match(patt, line).group(1) for line in sc if "SynthDef" in line]
