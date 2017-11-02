from __future__ import division
from __future__ import print_function
from FoxDot import *

#-->> Created with FoxDot <<--#

# Live coding is an interactive process and you can interact wih your code
# by executing it while it is being written. To execute a block of code (lines
# not separated by whitespace) use Ctrl+Return, or to execute a single line
# of code use Alt+Return

# FoxDot creates music by giving player objects a 'digital instrument'
# to play, which are called 'Synths'. You can see the list of pre-installed
# 'Synths' by executing

print(Synths)

# A player object is created by instantiating the Player class, like
# any other player class and takes no arguments. In FoxDot, all two-
# character variable names are reserved for player objects, such as 'p1'
# or 'bd'. Use >> to give one of these to a player object like so:

p1 >> pads()

# Give your player object instructions to make music with their Synth.
# The first argument is the note of the scale to play. The following code
# plays the first three notes of the default scale (major) on repeat.

p1 >> pads([0,1,2])

# Specify instructions for other player attributes (such as duration of
# notes) by using special keyword arguments

p1 >> pads([0,1,2], dur=[1,1/2,1/2], oct=6, pan=[1,-1])

# You can also assign values to the attributes of player objects directly

p1.chop = 4

# To see all the names of player attributes, just execute

print(Player.Attributes())

# You can modulate the degree of the player in an algorithmic way by
# using the '+' and '-' operators

p1 >> pads([0,1,2], dur=[1,1/2,1/2], oct=6, pan=[1,-1]) + [0,0,0,4]

p1 + [0,0,0,4]

# Stop a singler player, just call the 'stop' method or, to stop all
# player objects that are playing, use Clock.clear() or the Ctrl+.
# keyboard shortcut. 'Clock' is used to schedule the musical events

p1.stop()

Clock.clear()

# You can change the scale used by a player using the 'scale' keyword or
# you can change the default scale used by all players by setting the
# Scale.default object:

p1 >> pads([0,1,2], scale=Scale.minor)

Scale.default.set("minor")

Scale.default.set(Scale.minor)

Scale.default.set([0,2,3,5,7,10])

# To see a list of all scales, use

print(Scale.names())

# Similarly, you can change the root note players using the root keyword
# and the Root.default object

p >> pads([0,1,2], scale=Scale.minor, root=2)

Root.default.set(2)

Root.default.set("D")
