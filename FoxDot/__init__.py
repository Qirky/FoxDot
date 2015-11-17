"""

    Copyright Ryan Kirkbride 2015

    This is the module that combines all the other modules as if it were the live
    environment. The main.py application execute() method sends the string over to
    this module, which is analysed and sent back as the raw python code to execute.

    This module also handles the time keeping aspect. There is a constant tempo
    clock running that has a queue and plays the items accordingly

    Note: The code below IS executed in the Environment and can be accessed by the user!

"""

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
        self.values = None
        self.dur    = dur

        self.update(values, dur)

        return

    def __len__(self):

        return sum(self.dur)

    def __int__(self):

        return int(self.now())

    def __float__(self):

        return float(self.now())

    def update(self, values, dur=None):

        """ Changes the values for any player using this var """

        if dur:

            self.dur = dur

        dur = self.dur

        # Makes sure inputs are in list form

        values, dur = (asStream(x) for x in [values, dur])

        lv = len(values)
        ld = len(dur)

        stream = []

        for i in range(max(lv, ld)):
            stream += [values[i % lv]]*(dur[i % ld]*self.metro.steps)

        self.values = stream

        return
    
    def now(self):
        """ Returns the value at the current clock time """

        i = self.metro.now() % len(self.values)

        return self.values[i]
