# Tutorial 4: Using Vars

# A 'var' is a variable that changes over time. It takes two arguments
# at instantiation; states and a list of durations (this can a single number
# if all durations are equal).

a = var([0,4,5,3], 4)

# Try executing this line every few seconds

print(a)

# Use 'var' with your Player objects to create chord progressions. 

b1 >> bass(a, dur=PDur(3,8))

p1 >> pads(a + (0,2), dur=PDur(7,16))

# You can add a 'var' to a Player object or a var. 

b1 >> bass(a, dur=PDur(3,8)) + var([0,1],[3,1])

b = a + var([0,10],8)

print(a, b)

# Updating the values of one 'var' will update it everywhere else

a.update([1,4], 8)

print(a, b)

Clock.clear()

# You can also use a 'linvar' that changes its values gradually over time

c = linvar([0,1],16)

print(c)

p1 >> pads(a, amp=c)

Clock.clear()

# a 'Pvar' is a 'var' that can store patterns

d = Pvar([PRange(12), PTri(5)], 8)

print(d)

p1 >> pads(a, amp=c, dur=1/4) + d



