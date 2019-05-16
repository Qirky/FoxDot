# Tutorial 15: Patterns Generators Reference


# There are several other Pattern classes in FoxDot that help you generate arrays of numbers but also behave
# in the same way as the base Pattern. To see what Patterns exist and have a go at using them, execute
print(classes(Patterns.Sequences))



####################
# PEuclid
# PEuclid(n, k)
# Returns the Euclidean rhythm which spreads 'n' pulses over 'k' steps as evenly as possible.

# 3 pulses over 8 steps
print(PEuclid(3, 8))



####################
# PDur
# PDur(n, k, start=0, dur=0.25)
# Returns the actual durations based on Euclidean rhythms (see PEuclid) where dur is the length of each step.
# Spreads 'n' pulses over 'k' steps as evenly as possible

print(PDur(3,8)) # P[0.75, 0.75, 0.5]

print(PDur(5,8))

# Gives a list of 3 dur, appened with a list of 5 dur
print(PDur([3,5],8))

d1 >> play("x", dur=PDur(5,8))



####################
# PIndex
# Returns the index being accessed

print(PIndex())
print(PIndex()*4)



####################
# PSine
# PSine(n=16)
# Returns values of one cycle of sine wave split into 'n' parts

# Split into 5 parts
print(PSine(5))

# Split into 10
print(PSine(10))



####################
# PTri
# PTri(start, stop=None, step=None)
# Returns a Pattern equivalent to `Pattern(range(start, stop, step)) with its reversed form appended.
# Think of it like a "Tri"angle.

# Up to 5 then down to 1
print(PTri(5))

# Up to 8 then down to 1
print(PTri(8))

# From 3 to 10, then down to 4
print(PTri(3,10))

# From 3 to 30, by 2, then down to 4
print(PTri(3,20,2))

# Up to 4, then down to 1, then up to 8, then down to 1
print(PTri([4,8]))

p1 >> pluck(PTri(5), scale=Scale.default.pentatonic)

# Same as
p1 >> pluck(PRange(5) | PRange(5,0,-1), scale=Scale.default.pentatonic)



####################
# PRand
# PRand(start, stop=None)
# Returns a random integer between start and stop.

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



####################
# PRhythm
# PRhythm takes a list of single durations and tuples that contain values that can be supplied to the `PDur`

# The following plays the hi hat with a Euclidean Rhythm of 3 pulses in 8 steps
d1 >> play("x-o-", dur=PRhythm([2,(3,8)]))

print(PRhythm([2,(3,8)]))



####################
# PSum
# PSum(n, total)
# Returns a Pattern of length 'n' that sums to equal 'total'

# Returns a pattern of length 2, with elements summed up to 8
print(PSum(3,8))

# Returns a pattern of length 5, with elements summed up to 4
print(PSum(5,4))



####################
# PStep
# PStep(n, value, default=0)
# Returns a Pattern that every n-term is 'value' otherwise 'default'

# Every 4, make it 1, otherwise default to 0
print(PStep(4,1))

# Every 8, make it 6, otherwise, 4
print(PStep(8,6,4))

# Every 5, make it 2, otherwise, 1
print(PStep(5,2,1))



####################
# PWalk
# PWalk(max=7, step=1, start=0)

# By default, returns a pattern with each element randomly 1 higher or lower than the previous
print(PWalk()[:16])

# Changing step
print(PWalk(step=2)[:16])

# With max
print(PWalk(max=2)[:16])

# Start at a non-zero number
print(PWalk(start=6)[:16])



####################
# PWhite
# PWhite(lo=0, hi=1)
# Returns random floating point values between 'lo' and 'hi'

# Lo defaults to 0, hi defaults to 1
print(PWhite()[:8])

# Returns random numbers between 1 and 5
print(PWhite(1,5)[:8])



####################
# Custom Generator Patterns

# Custom generator patterns can be made by subclassing GeneratorPattern
# and overriding `GeneratorPattern.func`

class CustomGeneratorPattern(GeneratorPattern):
    def func(self, index):
        return int(index / 4)

print(CustomGeneratorPattern()[:10])

# This can be done more consisely using `GeneratorPattern.from_func`,
# passing in a function which takes an index and returns some pattern item.

def some_func(index):
    return int(index / 4)

print(GeneratorPattern.from_func(some_func)[:10])

# We can use lambdas too
print(GeneratorPattern.from_func(lambda index: int(index / 4))[:10])

