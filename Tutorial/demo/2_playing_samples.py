# Tutorial 1: Playing Samples

# You can play audio samples in the FoxDot/snd/ sub-directories by using the
# 'play' Synth and using a string of characters instead of list of notes.

bd >> play("x")

# A character refers to a sound file and whitespace is used for silence, so
# you can spread sounds out in time:

bd >> play("x  x  x ")

hh >> play(" -")

Clock.clear()

# You can lace patterns using round brackets

d1 >> play("(x )( x)o ")

# And shorten their durations by using square brackets

d1 >> play("x-o[-o]")

# The following patterns are identical

d1 >> play("x-o(-[-o])")

d1 >> play("x-o[-(o )]")

# Curly brackets squeeze any sound files into the duration of one

d1 >> play("x-o{---}")

Clock.clear()


