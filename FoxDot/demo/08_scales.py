# Tutorial 8: Scales


# By default, Player Objects use the C Major scale.
# These can be changed by using the keyword arguments 'scale' and 'root'.
# Scales can be defined as an array of semitones, such that the Major scale is [0,2,4,5,7,9,11]
# or one of the predefined scales from the Scale module, e.g. Scale.minor.
# Root refers to the tonic of the scale; 0 being C, 1 is C#, 2 is D and so on.

# The default scale can be changed such that any Player not using a specific scale will be updated.
# This is done using the syntax below (each line is technically equivalent):

Scale.default.set("major")
Scale.default.set(Scale.major)
Scale.default.set([0,2,4,5,7,9,11])

# Or the same thing, but minor:
Scale.default.set("minor")
Scale.default.set(Scale.minor)
Scale.default.set([0,2,3,5,7,10])

# To save some time you can also do
Scale.default = "minor"

#This is the same for the root:
Root.default.set(1)
Root.default.set("C#")

# Or:
Root.default.set(2)
Root.default.set("D")

# To see a list of all scales, use
print(Scale.names())

# You can change the scale used by a player using the 'scale' keyword
p1 >> pads([0,1,2], scale=Scale.minor)

# Similarly, you can change the root note players using the root keyword
# and the Root.default object
p1 >> pads([0,1,2], scale=Scale.minor, root=2)
