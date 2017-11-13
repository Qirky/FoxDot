# Tutorial 1: Playing Samples

# You can play audio samples in the FoxDot/snd/ sub-directories by using the
# 'play' Synth and using a string of characters instead of list of notes.

bd >> play("x")

# A character refers to a sound and whitespace is used for silence, so
# you can spread sounds out in time:

bd >> play("x  x  x ")

hh >> play(" -")

Clock.clear()

# You can lace patterns using round brackets

d1 >> play("(x )( x)o ")

# And shorten their durations by using square brackets

d1 >> play("x-o[-o]")

d1 >> play("x-o[---]")

# You can combine the brackets however you like: the following patterns are identical

d1 >> play("x-o(-[-o])")

d1 >> play("x-o[-(o )]")

# Curly braces select a sample sound at random if you want more variety

d1 >> play("x-o{-=[--][-o]}")

Clock.clear()

# Each character is mapped to a folder of sound files and you can select different
# samples by using the "sample" keyword argument

d1 >> play("(x[--])xu[--]")

d1 >> play("(x[--])xu[--]", sample=1)

d1 >> play("(x[--])xu[--]", sample=2)

d1 >> play("(x[--])xu[--]", sample=[1,2,3])

Clock.clear()



