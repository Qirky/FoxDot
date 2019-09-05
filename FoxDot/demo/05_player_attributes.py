# Tutorial 5: Referencing Player Attributes

# You can set variables outside a player
pitches = P[0,1,2,3,4]
harmony = pitches + 2

print(pitches)
print(harmony)

p1 >> pluck(pitches)
p2 >> star(harmony)

# If you set the duration of the second, it might not have the desired effect
p1 >> pluck(pitches)
p2 >> star(harmony, dur=1/2)

# It is possible for one player object to play exactly what another player is.
# To have one player follow another, just use the follow method:
p1 >> pluck(pitches)

p2 >> star(dur=1/2).follow(p1) + 2

# You can explicitly reference attributes such as pitch or duration too:

p2 >> star(p1.pitch) + 2  # this is the same as .follow(p1)

# Works for other attributes too
p1 >> pluck(pitches)
p2 >> star(dur=p1.dur).follow(p1) + 2

# You can reference, and test for the current value
# The == returns a 1 if true and a 0 if false
print(p1.degree)
print(p1.degree == 2)

# This allows you to do conditionals like
p1 >> pluck([0,1,2,3], amp=(p1.degree==1))

p1 >> pluck([0,1,2,3], amp=(p1.degree>1))

# Or change it to a different amp by multiplying by 4
p1 >> pluck([0,1,2,3], amp=(p1.degree==1)*4)

# Chain multiple conditionals
p1 >> pluck([0,1,2,3], amp=(p1.degree==1)*4 + (p1.degree==2)*1)

# Which is the same as
p1 >> pluck([0,1,2,3], amp=p1.degree.map({1:4, 2:1}))
