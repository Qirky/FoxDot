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
from Operations import LCM, modi, EuclidsAlgorithm
from Base import Pattern, GeneratorPattern, PGroup, asStream

MAX_SIZE = 2048

#==============================#
#         1. P[] & P()         #
#==============================#
 
class __pattern__ :
    ''' Pseudo-pattern.
        P[1,2,3] = Pattern([1,2,3])
        P(1,2,3) = Pattern((0,1,3))
    '''
    def __getitem__(self, args):
        return Pattern(list(args) if hasattr(args, '__iter__') else args)
    
    def __call__(self, *args):
        return PGroup(args if len(args) > 1 else args[0])
    
P = __pattern__()

#==============================#
#      1. Container Types      #
#==============================#

def PStutter(seq, n=2):
    """ PStutter(pattern, n) -> Creates a pattern such that each item in the array is repeated n times (can be a pattern) """
    return Pattern(seq).stutter(n)

def PShuf(seq):
    return Pattern(seq).shuffle()

def P10(n):
    return Pattern([random.choice((0,1)) for i in range(int(n))])

def PSq(a=1, b=2, c=3):
    return Pattern([x**b for x in range(a,a+c)])

def PAlt(pat1, pat2, *patN):
    data = []
    item = [asStream(p) for p in [pat1, pat2] + list(patN)]
    size = LCM(*[len(i) for i in item])
    for n in range(size):
        for i in item:
            data.append(modi(i,n))
    return Pattern(data)

def PStep(n, value, default=0):
    return Pattern([default]*(n-1)+[value])

def PSum(n, total, **kwargs):
    """
        PSum(n, total) -> Pattern of length n that sums to equal total

        e.g. PSum(3,8) -> [3,3,2]
             PSum(5,4) -> [1,0.75,0.75,0.75,0.75]

    """
    lim = kwargs.get("lim", 0.125)

    data = [total + 1]

    step = 1
    while sum(data) > total:
        data = [step for x in range(n)]
        step *= 0.5

    i = 0
    while sum(data) < total and step >= lim:
        if sum(data) + step > total:
            step *= 0.5
        else:
            data[i % n] += step
            i += 1
            
    return Pattern(data)

def PRange(start, stop=None, step=None):

    if stop is None and step is None and isinstance(start, (list, Pattern)):
        
        data = []

        for n in start:

            data += range(n)
    else:
        
        data = range(*[val for val in (start, stop, step) if val is not None])
        
    return Pattern(data)


def PTri(start, stop=None, step=None):
    rev_step = step if step is not None else 1
    data = list(PRange(start, stop, step))
    return Pattern(data + [item + rev_step for item in reversed(data)])

from math import sin, pi

def PSine(n=16):
    """ Values of one cycle of sine wave split into n parts """
    i = (2 * pi) / n
    return Pattern([sin(i * j) for j in range(int(n))])

def PStretch(data, size):
    return Pattern(data).stretch(size)

##def PChords(seq, struct=(0,2,4), stepsPerOctave=7):
##    # First item 'root' chord
##    self.data = []
##    for i, item in enumerate(seq):
##        chord = [item + val for val in struct]
##        if i > 0:
##            chords = [  chord,
##                       [note % stepsPerOctave for note in chord],
##                       [chord[0],chord[1],chord[2]-stepsPerOctave],
##                     ]
##            c2 = self.data[-1]
##            best = 1000
##            for c1 in chords:
##                d = self.distance(c1, c2)
##                if d < best:
##                    chord = c1
##                    best = d
##        # Add the chord with the smallest total change
##        self.data.append(tuple(sorted(chord)))
##@staticmethod
##def distance(a, b):
##    a = sorted(a)
##    b = sorted(b)
##    return sum([abs(a[i] - b[i]) for i in range(len(a))])        


def PPairs(seq, func=lambda n: 8-n):
    """ PPairs(iterable, func=lambda n: 8-n)

        Laces a sequence with a second sequence obtained
        by performing a function on the original """
        
    i = 0
    data = []
    for item in seq:
        data.append(item)
        data.append(func(item))
        i += 1
        if i >= MAX_SIZE:
            break
    return Pattern(data)

def PZip(pat1, pat2, *patN):
    l, p = [], []
    for pat in [pat1, pat2] + list(patN):
        p.append(asStream(pat))
        l.append(len(p[-1]))
    length = LCM(*l)
    return Pattern(zip(*[p[i].stretch(length) for i in range(len(p))]))


def PZip2(pat1, pat2, rule=lambda a, b: True):
    length = LCM(len(pat1), len(pat2))
    data = []
    i = 0
    while i < length:
        a, b = modi(pat1,i), modi(pat2,i)
        if rule(a, b):
            data.append((a,b))
        i += 1
    return Pattern(data)

### Patterns used for calculating rhythms

def PEuclid(n, k):
   return Pattern( EuclidsAlgorithm(n, k) )

def PDur(n, k, dur=0.25):
    """ Calculate durations based on Euclidean rhythms """

    pulses = asStream(n)
    steps  = asStream(k)

    size = LCM(len(pulses), len(steps))
    
    durations = []

    for i in range(size):

        n = pulses[i]
        k = steps[i]
        
        data = EuclidsAlgorithm(n, k)            

        count, new = 1, []

        for item in data[1:]:
            if item == 1:
                new.append(count)
                count = 1
            else:
                count += 1
        new.append(count)       
                
        durations += [count * dur for count in new]

    return Pattern(durations)
    

##class PRhythm(Pattern):
##
##    def __init__(self, s, dur=0.5):
##
##        character = []
##        durations = []
##
##        if type(s) is str:
##            s = Pattern().fromString(s)
##            
##        dur = s.dur(dur)
##        self.data = []
##        
##        for i, char in s.items():
##            # Recursively get rhythms
##            if isinstance(char, PGroup):
##                character += list(char)
##                durations += list(self.__class__(char, dur))
##            else:
##                character.append(char)
##                durations.append(dur)
##                
##        # After recursive collection of durations, adjust for rests (spaces)
##
##        self.chars = []
##        
##        for i, dur in enumerate(durations):
##            if character[i] == ' ' and i > 0:
##                self.data[-1] += dur                    
##            else:
##                self.data.append(dur)
##                self.chars.append(character[i])
##
##    def rest(self, n=0):
##        """ Returns true if self.chars[n] contains a space """
##        return self.chars[n] == ' '
##
##Prhythm = PRhythm #: Alias
##

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

class PWhite(GeneratorPattern):
    def __init__(self, lo=0, hi=1):
        GeneratorPattern.__init__(self)
        self.low = float(lo)
        self.high = float(hi)
        self.mid = (lo + hi) / 2.0
    def func(self, index):
        return random.triangular(self.low, self.high, self.mid)

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




