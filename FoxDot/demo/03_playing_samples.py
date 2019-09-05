# Tutorial 3: Playing Built-In Samples


# FoxDot can also be used to sequence and manipulate audio samples.
# To do this all you need to do is use the special play SynthDef.
# The first argument of the play SynthDef should be a string of characters
# instead of a list of numbers as you would do for any other SynthDef.
# Each character represents a different audio file, which is stored in a buffer in SuperCollider.

# To view which character relates to which audio file, execute
print(Samples)

# You can play audio samples in the FoxDot/snd/ sub-directories by using the
# 'play' Synth and using a string of characters instead of list of notes.
bd >> play("x")

# A character refers to a sound and whitespace is used for silence, so
# you can spread sounds out in time:
bd >> play("x  x  x  ")

hh >> play(" -")

# You can lace patterns using round brackets
# Whick plays like: "x o  xo "
d1 >> play("(x )( x)o ")

# The following is the same as "-------="
hh >> play("---(-=)")

# Putting characters in square brackets will play them all in the space of one beat
# And will be played like one character, not simultaneous, but in quick succession
d1 >> play("x-o[-o]")

d1 >> play("x-o[---]")

d1 >> play("x-o[-----]")

d1 >> play("x-o[--------------]")

# and can be put in round brackets as if they were one character themselves.
d1 >> play("x[--]o(=[-o])")

# You can combine the brackets however you like: the following patterns are identical
d1 >> play("x-o(-[-o])")

d1 >> play("x-o[-(o )]")

# Curly braces select a sample sound at random if you want more variety
d1 >> play("x-o{-=[--][-o]}")

# Angle brackets combine patterns to be play simultaneously
d1 >> play("<X   ><-   ><#   ><V   >")

d1 >> play("<X   >< -  ><  # ><   V>")

# Each character is mapped to a folder of sound files and you can select different
# samples by using the "sample" keyword argument
d1 >> play("(x[--])xu[--]")

d1 >> play("(x[--])xu[--]", sample=1)

d1 >> play("(x[--])xu[--]", sample=2)

# Change the sample for each beat
d1 >> play("(x[--])xu[--]", sample=[1,2,3])

# You can layer two patterns together - note the "P", look at tutorial 4 for more information.
d1 >> play(P["x-o-"] & P[" **"])

# And change effects applied to all the layered patterns at the same time
d1 >> play(P["x-o-"] & P[" **"], room=0.5)

# Example from the player tutorial, but with samples instead
# Conditionals...
d1 >> play("x[--]xu[--]x", sample=(d1.degree=="x"))

# Or change it to sample bank 2 by multiplying
d1 >> play("x[--]xu[--]x", sample=(d1.degree=="x")*2)

# Chain multiple conditionals
d1 >> play("x[--]xu[--]x", sample=(d1.degree=="x")*2 + (d1.degree=="-")*5)

# Which is the same as
d1 >> play("x[--]xu[--]x", sample=d1.degree.map({"x":2, "-":5}))
