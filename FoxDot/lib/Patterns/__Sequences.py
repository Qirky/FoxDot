"""
    Sequences.py
    ------------
    All patterns inherit from Base.Pattern. There are two types of pattern:

    1. Container types
        - Similar to lists but with different mathematical operators
    2. Generator types
        - Similar to generators but can be indexed (returns values based on functions)

"""

import random
import Operations as op
from Base import Pattern, GeneratorPattern, PGroup, asStream

MAX_SIZE = 2048

#==============================#
#         1. P[] & P()         #
#==============================#
 
class _Pattern:
    """ Pseudo-pattern.
        P[1,2,3] = Pattern([1,2,3])
        P(1,2,3) = Pattern((0,1,3))
    """
    def __getitem__(self, args):
        try:
            args = list(args)
        except:
            pass
        return Pattern(args)
    
    def __call__(self, *args):
        if len(args) == 1:
            args = args[0]
        return PGroup(args)
    
P = _Pattern()

#==============================#
#      1. Container Types      #
#==============================#

class PStutter(Pattern):
    """ PStutter(pattern, n) -> Creates a pattern such that each item in the array is repeated n times (can be a pattern) """

    def __init__(self, data, n=2):
        self.data = Pattern(data).stutter(n).data

Pstutter = PStutter #: Alias for PStutter()

class PShuf(Pattern):
    """ PShuf(seq) ->  """

    def __init__(self, data):
        self.data = data
        random.shuffle(self.data)
        self.make()

Pshuf = PShuf #: Alias for PShuf()

class PBin(Pattern):
    def __init__(self, n):
        self.data = [random.choice((0,1)) for i in range(n)]
        self.make()

Pbin = PBin

class PSq(Pattern):
    def __init__(self, a=1, b=2, c=3):
        self.data = [x**b for x in range(a,a+c)]
        self.make()

class PAlt(Pattern):
    def __init__(self, *patterns):
        self.data = []
        item = [asStream(p) for p in patterns]
        size = op.LCM(*[len(i) for i in item])
        for n in range(size):
            for i in item:
                self.data.append(op.modi(i,n))
        self.make()

class PStep(Pattern):
    def __init__(self, n, value, default=0):
        self.data = [default]*(n-1)+[value]
        self.make()
Pstep = PStep

class PFit(Pattern):
    """
        PFit(n, total) -> Pattern of length n that sums to equal total

        e.g. PSum(3,8) -> [3,3,2]
             PSum(5,4) -> [1,0.75,0.75,0.75,0.75]

    """

    lim = 0.125

    def __init__(self, n, total):

        self.data = [total + 1]

        step = 1
        while sum(self.data) > total:
            self.data = [step for x in range(n)]
            step *= 0.5

        i = 0
        while sum(self.data) < total and step >= self.__class__.lim:
            if sum(self.data) + step > total:
                step *= 0.5
            else:
                self.data[i % n] += step
                i += 1
            
        self.make()

Pfit = PFit #: Alias for PSum

class PRange(Pattern):

    def __init__(self, *args):

        if len(args) == 1 and isinstance(args[0], (list, Pattern)):
            self.data = []
            for n in args[0]:
                self.data += range(n)
        else:
            self.data = range(*args)
        self.make()

Prange = PRange #: Alias

class PTri(Pattern):

    def __init__(self, *args):

        try:
            
            step = args[2]

        except:

            step = 1

        A = range(*args)
        B = [x + step for x in reversed(A)]
        
        self.data = A + B

Ptri = PTri #: Alias for PTri

class PSine(Pattern):

    def __init__(self, size=16):

        N = size / 4
        self.data = PTri(0,N,1)/N | PTri(0,-N,-1)/N

Psine = PSine #: Alias for PSine

class PStretch(Pattern):

    def __init__(self, data, size):
        try:
            self.data = data.stretch(size)
        except:
            self.data = Pattern(data).stretch(size)

Pstretch = PStretch #: Alias

class PChords(Pattern):
    def __init__(self, seq, struct=(0,2,4), stepsPerOctave=7):
        # First item 'root' chord
        self.data = []
        for i, item in enumerate(seq):
            chord = [item + val for val in struct]
            if i > 0:
                chords = [  chord,
                           [note % stepsPerOctave for note in chord],
                           [chord[0],chord[1],chord[2]-stepsPerOctave],
                         ]
                c2 = self.data[-1]
                best = 1000
                for c1 in chords:
                    d = self.distance(c1, c2)
                    if d < best:
                        chord = c1
                        best = d
            # Add the chord with the smallest total change
            self.data.append(tuple(sorted(chord)))
    @staticmethod
    def distance(a, b):
        a = sorted(a)
        b = sorted(b)
        return sum([abs(a[i] - b[i]) for i in range(len(a))])        

Pchords = PChords #: Alias

class PPairs(Pattern):

    def __init__(self, seq, func=lambda n: 8-n):
        """ PPairs(iterable, func=lambda n: 8-n)

            Laces a sequence with a second sequence obtained
            by performing a function on the original """
        
        i = 0
        self.data = []
        for item in seq:
            self.data.append(item)
            self.data.append(func(item))
            i += 1
            if i >= MAX_SIZE:
                break
        self.make()

Ppairs = PPairs #: Alias

class PZip(Pattern):

    def __init__(self, *pats):
        l, p = [], []
        for pat in pats:
            p.append(asStream(pat))
            l.append(len(p[-1]))
        length = op.LCM(*l)
        self.data = asStream(zip(*[p[i].stretch(length) for i in range(len(p))]))


class PZip2(Pattern):
    def __init__(self, pat1, pat2, rule=lambda a, b: True):
        length = op.LCM(len(pat1), len(pat2))
        self.data = []
        i = 0
        while i < length:
            a, b = op.modi(pat1,i), op.modi(pat2,i)
            if rule(a, b):
                self.data.append((a,b))
            i += 1
        self.make()

### Patterns used for calculating rhythms

class PEuclid(Pattern):
    def __init__(self, n, k):
        self.data = op.EuclidsAlgorithm(n, k)

class PDur(Pattern):
    def __init__(self, n, k, dur=0.25):
        """ Calculate durations based on Euclidean rhythms """

        pulses = asStream(n)
        steps  = asStream(k)

        size = op.LCM(len(pulses), len(steps))
        
        self.data = []

        for i in range(size):

            n = pulses[i]
            k = steps[i]
            
            data = op.EuclidsAlgorithm(n, k)            

            count, new = 1, []

            for item in data[1:]:
                if item == 1:
                    new.append(count)
                    count = 1
                else:
                    count += 1
            new.append(count)       
                    
            self.data += [count * dur for count in new]
        

class PRhythm(Pattern):

    def __init__(self, s, dur=0.5):

        character = []
        durations = []

        if type(s) is str:
            s = Pattern().fromString(s)
            
        dur = s.dur(dur)
        self.data = []
        
        for i, char in s.items():
            # Recursively get rhythms
            if isinstance(char, PGroup):
                character += list(char)
                durations += list(self.__class__(char, dur))
            else:
                character.append(char)
                durations.append(dur)
                
        # After recursive collection of durations, adjust for rests (spaces)

        self.chars = []
        
        for i, dur in enumerate(durations):
            if character[i] == ' ' and i > 0:
                self.data[-1] += dur                    
            else:
                self.data.append(dur)
                self.chars.append(character[i])

    def rest(self, n=0):
        """ Returns true if self.chars[n] contains a space """
        return self.chars[n] == ' '

Prhythm = PRhythm #: Alias


#==============================#
#      2. Generator Types      #
#==============================#

class PRand(GeneratorPattern):
    def __init__(self, start, stop=None):
        GeneratorPattern.__init__(self)
        if hasattr(start, "__iter__"):
            self.data = start
            self.func = lambda index: random.choice(Pattern(self.data))
        else:
            self.low  = start if stop is not None else 0
            self.high = stop  if stop is not None else start
    def func(self, index):
        return random.randrange(self.low, self.high)

Prand = PRand

class PWhite(GeneratorPattern):
    def __init__(self, lo=0, hi=1):
        GeneratorPattern.__init__(self)
        self.low = float(lo)
        self.high = float(hi)
        self.mid = (lo + hi) / 2.0
    def func(self, index):
        return random.triangular(self.low, self.high, self.mid)

Pwhite = PWhite #: Alias

class PSquare(GeneratorPattern):
    def func(self, index):
        return index * index

##
##
##class PxRand(GeneratorPattern):
##    """
##        PxRand(iterable)
##        PxRand(lo, hi)
##
##        Differs from PRand() in that PxRand returns a random element
##        of a given list or range(lo, hi) each time it is accessed as
##        opposed to a predetermined list of random numbers/elements
##
##    """
##
##    def __init__(self, a, b=None):
##        if not isinstance(a, list):
##            a = range(a, b) if b is not None else range(a)
##        self.data = [random.choice(a)]
##        for n in range(MAX_SIZE):
##            self.data.append(random.choice([item for item in a if item != self.data[-1]]))
##        self.make()
##
##Pxrand = PxRand #: Alias for PxRand
##
##class PwRand(GeneratorPattern):
##    """ Docstring """
##    def __init__(self, pattern, weights):
##        seq = []
##        for i, value in enumerate(pattern):
##            seq.extend([value] * int(weights[i] * 100))
##        self.data = [random.choice(seq) for n in range(MAX_SIZE)]
##        self.make()
##
##Pwrand = PwRand
##
##
##


##class PLace(Base.Pattern):
##    def __init__(self, data):
##        i, loop = 0, LCM(*[(len(self(item)) if hasattr(item, "__len__") else 1) for item in data])
##        new_data = []
##        while i < loop:
##            for item in data:
##                if isinstance(item, (Pattern, list)):
##                    item = modi(self(item), i)
##                new_data.append(item)
##            i += 1
##        self.make()

##class PDur(Base.Pattern):
##
##    def __init__(self, s, dur=0.5):
##
##        self.chars = []
##        self.data  = []
##
##        if type(s) is str:
##            s = P().fromString(s)
##            
##        dur = s.dur(dur)
##        self.data = []
##        
##        for i, char in s.items():
##            # Recursively get rhythms
##            val = op.modi(dur,i)
##            if isinstance(char, Base.PGroup):
##                dur_group = self.__class__(char, val)
##                self.chars += list(dur_group.chars)
##                self.data  += list(dur_group.data)
##            else:
##                self.chars.append(char)
##                self.data.append(val)
##
##Pdur = PDur #: Alias                


#### ---- Testing


#### -------------- These need updating

##def irange(start, stop=None, step=0.1):
##    r = []
##    if not stop:
##        stop = start
##        start = 0
##    while start <= stop:
##        r.append( start )
##        start += step
##    return r
##
##
##def fShuf(a, b=None, size=8):
##
##    if b:
##
##        L = [a + (n * ( (b-a) / float(size))) for n in range(size)]
##
##    else:
##
##        L = [n * ( a / float(size)) for n in range(size)]
##
##    random.shuffle(L)
##
##    return L
##
##
##def Walk(hi=8, variation=1, size=256):
##
##    stream = [0]
##
##    variation = 1.0 / variation
##
##    step = random.choice([1,-1])
##
##    while len(stream) < size:
##
##        step = step * (-1)
##
##        for x in range( int(hi * random.triangular(variation, 1)) - 1 ):
##
##            stream.append( stream[-1] + step )
##
##            if len(stream) == size:
##                break
##
##    return stream
##
##
##def Sparse(arr=[0,1], hi=8):
##
##    stream =[]
##
##    return strema
##
##
##def Geom(n, lo=1, hi=None):
##
##    if not hi:
##
##        hi = max(lo, 1)
##        lo = min(lo, 1)
##
##    return [n**i for i in range(lo, hi+1)]
##
##def GeomFill(arr, N=2):
##    """ GeomFill(arr) -> new_arr such that sum(new_list) is power of N """
##    nums  = arr
##    total = 1
##    while sum(nums) >= total:
##        total *= N
##    nums.append( total - sum(nums) )
##    return nums
##
##
##def Rint(a, b=None):
##
##    if b:
##
##        return random.randrange(a, b)
##
##    else:
##
##        return random.randrange(0, a)
##
##
##def Rhythm(string, step=0.5):
##
##    stream = []
##
##    dur = 0.0
##
##    in_br = False
##
##    for i, char in enumerate(string):
##
##       # Needs work 
##
##        if char == "[":
##
##            in_br = True
##
##            dur -= step
##
##        elif char == "]":
##
##            in_br = False
##
##            dur -= step
##        
##        elif char != " ":
##
##            stream.append(dur)
##
##            dur = 0.0
##
##        elif i == len(string) - 1:
##
##            stream.append(dur + step)
##
##
##        if in_br:
##
##            dur += step/2.0
##
##        else:   
##    
##            dur += step
##
##    return stream[1:]
##




