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

# Define default variables

Clock = TempoClock()

default_scale = Scale.Scale("major")

print "Welcome to FoxDot!"
