# Tutorial 1: Playing Notes

# In FoxDot, all two-character variable names are reserved for player objects, such as 'p1'
# Creating a Player Object with no arguments will play a single note on middle C, by default, repeatedly until stopped.
# Use >> to give one of these to a player object like so:

p1 >> pluck()

# To stop an individual player object, simply execute

p1.stop()

# Besides the 2-character variables that are pre-reserved, you can create your
# own with your own names

foo = Player()
foo >> pluck()

# The >> in Python is usually reserved for a type of operation, like + or -, but it is not the case in FoxDot.
# If a user re-executes the code, FoxDot will update p1 instead of creating a PlayerObject,
# which means you can make changes to your music using just one line of code.

# If you now give your player object some arguments, you can change the notes being played back.
# The first argument should be the degree of the note to be played
# (default is the lowest note of octave 5 of the major scale) and does not need to be specified by name.

# Python, like most programming languages, using zero-indexing when accessing values in an array,
# which means that 0 refers to the first note of the scale.
# Give your player object instructions to make music with their Synth.
# The first argument is the note of the scale to play. The following code
# plays the first three notes of the default scale (major) on repeat.

# For a single note
p1 >> pluck(0)

# Or a list of notes
p1 >> pluck([0,1,2])

# But you’ll need to specify whatever else you want to change...

# Such as note durations, or the length of each note
p1 >> pluck([0,0,0], dur=[1,2,3])

# Or amplitude, the "volume" of each note
p1 >> pluck([0,0,0], amp=[1,2,3])

# If the second list, the amp in this example, is too long, then the first list (the degree) just loops, and are matched with the remaining elements from the second list (the amplitude).
p1 >> pluck([0,2,4], amp=[1,2,3,1,5])

# More generally, all the lists are traversed regardless of their length.
p1 >> pluck([0,2,4], dur=[1,2], amp=[1,2,3,1,5])

# Arguments can be integers, floating points, fractions, lists,
# tuples, or a mix

p1 >> pluck([0,0,0], dur=2)

p1 >> pluck([0,0,0], dur=1.743)

p1 >> pluck([0,0,0], dur=[0.25,0.5,0.75])

p1 >> pluck([0,0,0], dur=[1/4,1/2,3/4])

p1 >> pluck([0,0,0], dur=[1/4,0.25,3])

# Lists of values are iterated over as the Player plays notes
# The following duration equates to:  1,2,3,1,4,3
# If you don't understand this yet, don't worry, more about patterns in the pattern tutorial
p1 >> pluck([0,0,0], dur=[1,[2,4],3])

# Values in tuples are used simultaneously i.e. p1 will play 3 individual notes, then a chord of 3 together at the same time.
p1 >> pluck([0,2,4,(0,2,4)])

# You can also assign values to the attributes of player objects directly
p1.oct = 5

# To see all the names of player attributes, just execute
print(Player.get_attributes())

# More about those later in the player attributes tutorial

# You could store several player instances and assign them at different times
proxy_1 = pads([0,1,2,3], dur=1/2)
proxy_2 = pads([4,5,6,7], dur=1)

p1 >> proxy_1 # Assign the first to p1

p1 >> proxy_2 # This replaces the instructions being followed by p1

# To play multiple sequences at once, just do the same things with another
# Player object:

p1 >> pluck([0, 2, 3, 4], dur=1/2)

p2 >> pads([(0, 2, 4), (3, 5, 7)], dur=8)

# Play only this player, muting others
p1.solo() # default value is 1 (solo on)

# And turn the solo off
p1.solo(0)

# Stop (not just mute) the other players
p1.only()

# Use Ctrl+. to clear everything for the scheduling clock or run
Clock.clear()
