# Tutorial 15: Patterns Generators Reference


# There are several other Pattern classes in FoxDot that help you generate arrays of numbers but also behave
# in the same way as the base Pattern. To see what Patterns exist and have a go at using them, execute
print(classes(Patterns.Sequences))



# PDur(n, k, start=0, dur=0.25)
# Returns the actual durations based on Euclidean rhythms where dur is the length of each step.
# Spreads 'n' pulses over 'k' steps as evenly as possible
print(PDur(3,8)) # P[0.75, 0.75, 0.5]
print(PDur(5,8))
print(PDur([3,5],8)) # Gives a list of 3 dur, appened with a list of 5 dur

d1 >> play("x", dur=PDur(5,8))



# PIndex
# Returns the index being accessed
print(PIndex())
print(PIndex()*4)

d1 >> play("x", dur=PDur(5,8))


# PSine
# Returns values of one cycle of sine wave split into 'n' parts
print(PSine(5))

print(PSine(10))



# PTri(start, stop=None, step=None)
# Returns a Pattern equivalent to `Pattern(range(start, stop, step)) with its reversed form appended.
# Think of it like a "Tri"angle.
print(PTri(5))
print(PTri(8))
print(PTri(3,10))
print(PTri(3,20,2))
print(PTri([4,8]))

p1 >> pluck(PTri(5), scale=Scale.default.pentatonic)

# Same as
p1 >> pluck(PRange(5) | PRange(5,0,-1), scale=Scale.default.pentatonic)



# PRand
# Returns a random integer between 0 and start.
print(PRand(8)[:5])

# Returns a random integer between start and stop.
print(PRand(8,16)[:5])

# If start is a container-type it returns a random item for that container.
print(PRand([1,2,3])[:5])

# You can supply a seed
print(PRand([1,2,3], seed=5)[:5])

# Keeps generating random tune
p1 >> pluck(PRand(8))

# Creates a random list, and iterates over that same list
p1 >> pluck(PRand(8)[:3])



# PRhythm
# PRhythm takes a list of single durations and tuples that contain values that can be supplied to the `PDur`

# The following plays the hi hat with a Euclidean Rhythm of 3 pulses in 8 steps
d1 >> play("x-o-", dur=PRhythm([2,(3,8)]))

print(PRhythm([2,(3,8)]))



# PStep
# Returns a Pattern that every n-term is 'value' otherwise 'default'

# Every 3, make it 1, otherwise, 4
print(PStep(3,1,4))
