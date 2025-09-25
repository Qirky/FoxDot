# Tutorial 6: Rests


# Rests can be added by using a rest object in the dur array
# The rest silences the note that would have been played.

# Without a rest, 5 notes (yes, a dur=1 would work, but lets be explicit to counterpoint the next example)
p1 >> pads([0,1,2,3,4], dur=[1,1,1,1,1])

# With a rest ... 4 notes and a rest, note "4" is silenced for 4 beats
p1 >> pads([0,1,2,3,4], dur=[1,1,1,1,rest(4)])
