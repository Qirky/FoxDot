# Tutorial 11: Using Vars


# A TimeVar is an abbreviation of “Time Dependent Variable” and is a key feature of FoxDot.
# A TimeVar has a series of values that it changes between after a pre-defined number of beats
# and is created using a var object with the syntax var([list_of_values],[list_of_durations]).

# Generates the pattern: 0,0,0,0,3,3,3,3...
a = var([0,3],4)            # Duration can be single value
print(int(Clock.now()), a)   # 'a' initially has a value of 0
# >>> 0, 0

print(int(Clock.now()), a)   # After 4 beats, the value changes to 3
# >>> 4, 3

print(int(Clock.now()), a)   # After another 4 beats, the value changes to 0
# >>> 8, 0

# Duration can also be a list
a = var([0,3],[4,2])
print(int(Clock.now()), a)

# When a TimeVar is used in a mathematical operation, the values it affects also become TimeVars
# that change state when the original TimeVar changes state – this can even be used with patterns:
a = var([0,3], 4)
print(int(Clock.now()), a + 5)   # When beat is 0, a is 5
# >>> 5

print(int(Clock.now()), a + 5)   # When beat is 4, a is 8
# >>> 8

b = PRange(4) + a
print(int(Clock.now()), b)   # After 8 beats, the value changes to 0
# >>> P[0, 1, 2, 3]

print(int(Clock.now()), b)   # After 12 beats, the value changes to 3
# >>> P[3, 4, 5, 6]

# Use 'var' with your Player objects to create chord progressions.
a = var([0,4,5,3], 4)
b1 >> bass(a, dur=PDur(3,8))
p1 >> pads(a + (0,2), dur=PDur(7,16))

# You can add a 'var' to a Player object or a var.
b1 >> bass(a, dur=PDur(3,8)) + var([0,1],[3,1])

b = a + var([0,10],8)

print(int(Clock.now()), (a, b))

# Updating the values of one 'var' will update it everywhere else
a.update([1,4], 8)

print(int(Clock.now()), (a, b))

# Vars can be named ...
var.chords = var([0,4,5,4],4)

# And used later
b1 >> pluck(var.chords)

# Any players using the named var will be updated
var.chords = var([0,1,5,3],4)

# You can also use a 'linvar' that changes its values gradually over time
# Change the value from 0 to 1 over 16 beats
c = linvar([0,1],16)

# Run this multiple times to see the changes happening
print(int(Clock.now()), c)

# Change the amp based off that linvar
p1 >> pads(a, amp=c)

# a 'Pvar' is a 'var' that can store patterns (as opposed to say, integers)
d = Pvar([P[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], P[0, 1, 2, 3, 4, 5, 4, 3, 2, 1]], 8)

print(int(Clock.now()), d)

p1 >> pads(a, amp=c, dur=1/4) + d

# Change the scale every 16 beats
Scale.default = Pvar([Scale.major, Scale.minor],16)
