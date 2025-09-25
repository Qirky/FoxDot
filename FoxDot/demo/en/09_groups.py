# Tutorial 9: Groups


# Attributes of players, such as degree or scale, can also be changed by directly assigning values to it such that
p1 >> pads([0,2,4,2], scale=Scale.majorPentatonic)

# is equivalent to
p1 >> pads()
p1.degree = [0,2,4,2]
p1.scale = Scale.majorPentatonic

# This is useful if you want to assign the same values to multiple Player Object simultaneously, like so:
p1 >> pads([0,2,4,2])
p2 >> pads([2,1,0,4])
p3 >> pads([2,3])
p1.dur=p2.dur=p3.dur=[1,1/2,1/4,1/4]

p1.stop()
p2.stop()
p3.stop()

# You can reference all the members with similar names
p_all.dur = [1/2,1/4] # Run this while p1, p2, etc are playing!

# or
p_all.amplify = 1

# Or...
p_all.stop()

# Or...
p_all.solo()

# To reduce the amount of typing, Player Objects can be grouped together and their attributes modified in a simpler way:
p1 >> pads([0,2,4,2])
p2 >> pads([2,1,0,4])
p3 >> pads([2,3])
g1 = Group(p1, p2, p3)
g1.dur=[1,1/2,1/4,1/4]

# You can group will _all groups
g1 = Group(p_all, d_all, b1, b2)

# Set the volume on for 4 beats, then off for 4
# This overrides existing amplitudes set in the player object
g1.amp=var([1,0],4)

g1.stop()

# You can use functions to group things together. To execute use CTRL+Return, not ALT+Return.
def tune():
    b1 >> bass([0,3], dur=4)
    p1 >> pluck([0,4], dur=1/2)
    d1 >> play("x--x--x-")
tune()

# or schedule the clock to call other grouped functions
def verse():
    b1 >> bass([0,3], dur=4)
    p1 >> pluck([0,4], dur=1/2)
    d1 >> play("x--x--x-")
    Clock.future(16, chorus)
def chorus():
    b1 >> bass([0,4,5,3], dur=4)
    p1 >> pluck([0,4,7,9], dur=1/4)
    d1 >> play("x-o-")
    Clock.future(16, verse)
verse()
