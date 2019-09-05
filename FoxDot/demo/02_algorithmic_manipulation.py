# Tutorial 2: Algorithmic Manipulation

# The code below plays the first four notes of the default scale on repeat:
p1 >> pads([0,1,2,3])

# It's possible to manipulate this by adding an array of numbers to the Player object
# This raises the 4th note played by 2 degrees
p1 >> pads([0,1,2,3]) + [0,0,0,2]

# And this raises every third note by 2
p1 >> pads([0,1,2,3]) + [0,0,2]

# These values can be laced and grouped together
p1 >> pads([0,1,2,3]) + [0,1,[0,(0,2)]]

# This behaviour is particularly useful when using the follow method.
b1 >> bass([0,4,5,3], dur=2)
p1 >> pads().follow(b1) + [2,4,7]

# You can schedule players to do things
# This will tell p1 to reverse the notes every 4 beats
p1 >> pads([0,2,4,6])
p1.every(4, "reverse")

# You can "chain" methods together by appending them to the end of
# the original line:
p1 >> pads([0,2,4,6]).every(4, "reverse")

# To stop calling "reverse", use 'never':

p1.never("reverse")

# Here are a few other methods you can use:

# Using "stutter" will play the same note 'n' number of times with different attributes specified

p1.every(4, "stutter", 4, oct=4, pan=[-1,1])

# Rotate will move all the values over by 1 in their order
p1.every(4, "rotate")

# To randomise the order of the notes, use "shuffle"
p1.every(4, "shuffle")


