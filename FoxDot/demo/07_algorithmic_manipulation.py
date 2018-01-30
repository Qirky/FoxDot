# Tutorial 7: Algorithmic Manipulation


# The code below plays the first four notes of the default scale on repeat:
p1 >> pads([0,1,2,3])

# It's possible to manipulate this by adding an array of numbers to the Player object
# This raises the 4 note played by 2 degrees
p1 >> pads([0,1,2,3]) + [0,0,0,2]

# And this raises every third note by 2
p1 >> pads([0,1,2,3]) + [0,0,2]

# These values can be laced and grouped together
p1 >> pads([0,1,2,3]) + [0,1,[0,(0,2)]]

# This behaviour is particularly useful when using the follow method.
b1 >> bass([0,4,5,3], dur=2)
p1 >> pads().follow(b1) + [2,4,7]
