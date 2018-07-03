from .Patterns import Pattern, PGroup, asStream

I   = PGroup(0, 2, 4)
II  = PGroup(1, 3, 5)
III = PGroup(2, 4,-1)
IV  = PGroup(3, 5, 0)
V   = PGroup(4,-1, 1)
VI  = PGroup(5, 0, 2)
VII = PGroup(-1,1, 3)

I7   = PGroup(I).append(6)
II7  = PGroup(II).append(7)
III7 = PGroup(III).append(8)
IV7  = PGroup(IV).append(9)
V7   = PGroup(V).append(10)
VI7  = PGroup(VI).append(11)
VII7 = PGroup(VII).append(12)