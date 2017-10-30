from __future__ import print_function
# FoxDot Pattern objects are a container type similar to Python lists
# but behaves differently when performing mathematical operations. A
# basic pattern is created as you would with a normal list or tuple,
# but with a 'P' preceeding it.

print([0,1,2,3] * 2)

print(P[0,1,2,3] * 2)

# Pattern objects also automatically lace any nested lists

for n in [0,1,2,[3,4]]:
    print(n)

for n in P[0,1,2,[3,4]]:
    print(n)

# Use PGroups if you want this behavior to be avoided. These can be implicitly
# specified as tuples in Patterns:

for n in P[0,1,2,(3,4)]:
    print(n)

print(P(0,2,4) + 2)

# Adding a list (or Pattern) to a Pattern will add the values of the
# elements to the other where Python lists would be concatonated. To
# concatonate Patterns, use the pipe operator like so:

print(PRange(10) + [0,10])

print(PRange(10) | [0,10])

# Patterns come with several methods for manipulating the contents

help(Pattern)

# Use Patterns to generate algorithmic music with Player objects

p1 >> pads(Ptri(8), dur=1/2)

d1 >> play("x", dur=PDur(5,8))


