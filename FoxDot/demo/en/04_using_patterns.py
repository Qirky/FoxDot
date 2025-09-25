# Tutorial 4: Using Patterns


# Player Objects use Python lists, known more commonly as arrays in other languages,
# to sequence themselves. You've already used these previously, but they aren't exactly
# flexible for manipulation. For example, try multiplying a list by two like so:

print([1, 2, 3] * 2)

# Is the result what you expected?

# FoxDot uses a container type called a 'Pattern' to help solve this problem.
# They act like regular lists but any mathematical operation performed on it is done to each item
# in the list and done so pair-wise if using a second pattern. A basic pattern is created as
# you would with a normal list or tuple, but with a 'P' preceeding it.

print(P[1,2,3] * 2)

print(P[1,2,3] + 100)

# In this operation, the output consists of all the combinations of the two patterns i.e.
# [1+3, 2+4, 3+3, 1+4, 2+3, 3+4]
print(P[1,2,3] + [3,4])

# You can use Python's slicing syntax to generate a series of numbers

print(P[:8])

print(P[0,1,2,3:20])

print(P[2:15:3])

# Try some other mathematical operators and see what results you get.
print(P[1,2,3] * (1,2))

# Pattern objects also automatically interlace any nested list.
# Compare
# Normal list:
for n in [0,1,2,[3,4],5]:
    print(n)

# with
# Pattern
for n in P[0,1,2,[3,4],5]:
    print(n)

# Use PGroups if you want this behavior to be avoided. These can be implicitly
# specified as tuples in Patterns:
for n in P[0,1,2,(3,4)]:
    print(n)

# This is a PGroup:
print(P(0,2,4) + 2)

print(type(P(0,2,4) + 2))

# In Python, you can generate a range of integers with the syntax range(start, stop, step).
# By default, start is 0 and step is 1.
print(list(range(10))) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# You can use PRange(start, stop, step) to create a Pattern object with the equivalent values:
print(PRange(10)) # P[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# P[0, 2, 2, 6, 4, 10, 6, 14, 8, 18]
# [0*1, 1*2, 2*1, 3*2, 4*1, 5*2, 6*1, 7*2, 8*1...]
print(PRange(10) * [1, 2])           # Pattern class behaviour

# Adding a list (or Pattern) to a Pattern will add the values of the
# elements to the other where Python lists would be concatonated.
print(PRange(10) + [0,10])

# To concatonate Patterns, use the pipe operator like so:
print(PRange(10) | [0,10])
# FoxDot automatically converts any object being piped to a Pattern to the base Pattern class
# so you don't have to worry about making sure everything is the right type.

# Plays all the values together
p1 >> pluck(P(4,6,8))
p1 >> pluck(P[0,1,2,P(4,6,8),7,8])

# Spreads the values across the current "dur" e.g. if the dur is 2 beats then it will play each value 2/3 beats apart
p1 >> pluck(P*(0,2,4), dur=1/2)
p1 >> pluck(P*(0,2,4), dur=1)
p1 >> pluck(P*(0,2,4), dur=2)
p1 >> pluck(P[0,1,2,P*(4,6,8),7,8], dur=1)

# Is the same as P* but every other time the notes are played they are spread over the dur value.
p1 >> pluck(P/(0,2,4), dur=1/2)
p1 >> pluck(P/(0,2,4), dur=1)
p1 >> pluck(P/(0,2,4), dur=2)
p1 >> pluck(P[0,1,2,P/(4,6,8),7,8], dur=1)

# Spreads the values across the current "sus" e.g. if the dur is 2 beats and the sus is 3 beats then it will play each value 1 beat apart.
p1 >> pluck(P+(0,2,4), dur=2, sus=3)
p1 >> pluck(P+(0,2,4), dur=2, sus=1)
p1 >> pluck(P[0,1,2,P+(4,6,8),7,8], dur=1, sus=3)

# Spreads the first (length - 1) values with a gap of the last value between each
# Plays 0,2,4 with a gap of 0.5:
p1 >> pluck(P^(0,2,4,0.5), dur=1/2)

# Patterns come with several methods for manipulating the contents
help(Pattern)

# Standard pattern
print(P[:8])

# Shuffle pattern by randomizing it
print(P[:8].shuffle())

# Append a reversed pattern to the pattern
print(P[:8].palindrome())

# Shift the pattern by n (default 1)
print(P[:8].rotate())
print(P[:8].rotate(3))
print(P[:8].rotate(-3))

# Takes the pattern and appends it as many times as needed to reach n number of elements in the pattern
print(P[:8].stretch(12))
print(P[:8].stretch(20))

# Reverses a pattern
print(P[:8].reverse())

# Loops a pattern n number of times
print(P[:8].loop(2))

# Add an offset
print(P[:8].offadd(5))

# Add a multiplied offset
print(P[:8].offmul(5))

# Stutter - Repeat each element n times
print(P[:8].stutter(5))

# Amen
# Merges and laces the first and last two items such that a
# drum pattern "x-o-" would become "(x[xo])-o([-o]-)" and mimics
# the rhythm of the famous "amen break"
d1 >> play(P["x-o-"].amen())
print(P[:8].amen())

# Bubble
# Merges and laces the first and last two items such that a
# drum pattern "x-o-" would become "(x[xo])-o([-o]-)
d1 >> play(P["x-o-"].bubble())
print(P[:8].bubble())

