import random
import Base
import Operations as op

"""
    All patterns inherit from Base.Pattern

"""

MAX_SIZE = 2048
 
class P(Base.Pattern):
    """ P(iterable) -> User-defined pattern """
    pass

class PStutter(Base.Pattern):
    """ PStutter(pattern, n) -> Creates a pattern such that each item in the array is repeated n times (can be a pattern) """

    def __init__(self, data, n=1):

        n = P(n)

        lrg = max(len(data), len(n))

        self.data = []

        for i in range(lrg):
            for j in range(op.modi(n,i)):
                self.data.append(op.modi(data,i))

##        for i, item in enumerate(data):
##            for j in range(op.modi(n,i)):
##                self.data.append( item )

        self.make()

Pstutter = PStutter #: Alias for PStutter()

class PShuf(Base.Pattern):
    """ PShuf(seq) ->  """

    def __init__(self, data):
        self.data = data
        self.make()
        random.shuffle(self.data)

Pshuf = PShuf #: Alias for PShuf()

class PRand(Base.Pattern):
    """
        Prand(iterable) -> Returns a stream of random elements
        Prand(lo, hi) -> Returns a stream of random elements between lo and hi
    """

    def __init__(self, a, b=None):        
        if isinstance(a, list):
            self.data = [random.choice(a) for n in range(MAX_SIZE)]
        else:
            self.data = [random.randrange(a, b) for n in range(MAX_SIZE)]
        self.make()

Prand = PRand #: Alias for PRand

class PxRand(Base.Pattern):
    """
        PxRand(iterable)
        PxRand(lo, hi)

        Differs from PRand() in that PxRand returns a random element
        of a given list or range(lo, hi) each time it is accessed as
        opposed to a predetermined list of random numbers/elements

    """

    def __init__(self, a, b=None):
        if isinstance(a, list):
            self.data = a
        else:
            self.data = range(a,b)
        self.make()
    def __iter__(self):
        for item in self.data:
            yield self.choose()
    def __getitem__(self, key):
        return self.choose()
    def __getslice__(self, start, end):
        return PxRand([self.choose() for n in range(start, end)])

Pxrand = PxRand #: Alias for PxRand

class PSq(Base.Pattern):
    def __init__(self, a=1, b=2, c=3):
        self.data = [x*b for x in range(a,a+c)]
        self.make()


class PSum(Base.Pattern):
    """
        PSum(n, total) -> Pattern of length n that sums to equal total

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

Psum = PSum #: Alias for PSum

class PRange(Base.Pattern):

    def __init__(self, *args):

        self.data = range(*args)
        self.make()

Prange = PRange #: Alias

class PWhite(Base.Pattern):

    def __init__(self, lo=0, hi=1):

        lo = float(lo)
        hi = float(hi)

        mode = (lo + hi) / 2.0

        self.data = [random.triangular(lo, hi, mode) for n in range(MAX_SIZE)]
        self.make()

Pwhite = PWhite #: Alias

class PTri(Base.Pattern):

    def __init__(self, *args):

        try:
            
            step = args[2]

        except:

            step = 1

        A = range(*args)
        B = [x + step for x in reversed(A)]
        
        self.data = A + B

Ptri = PTri #: Alias for PTri

class PSine(Base.Pattern):

    def __init__(self, size=16):

        N = size / 4
        self.data = PTri(0,N,1)/N | PTri(0,-N,-1)/N

Psine = PSine #: Alias for PSine

class PStretch(Base.Pattern):

    def __init__(self, data, size):
        try:
            self.data = data.stretch(size)
        except:
            self.data = P(data).stretch(size)

Pstretch = PStretch #: Alias

class PRhythm(Base.Pattern):

    def __init__(self, s, dur=0.5):

        character = []
        durations = []

        if type(s) is str:
            s = P().fromString(s)
            
        dur = s.dur(dur)
        self.data = []
        
        for i, char in s.items():
            # Recursively get rhythms
            if isinstance(char, Base.PGroup):
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

class PDur(Base.Pattern):

    def __init__(self, s, dur=0.5):

        self.chars = []
        self.data  = []

        if type(s) is str:
            s = P().fromString(s)
            
        dur = s.dur(dur)
        self.data = []
        
        for i, char in s.items():
            # Recursively get rhythms
            if isinstance(char, Base.PGroup):
                dur_group = self.__class__(char, dur)
                self.chars += list(dur_group.chars)
                self.data  += list(dur_group.data)
            else:
                self.chars.append(char)
                self.data.append(dur)

Pdur = PDur #: Alias                

class PChords(Base.Pattern):

    def __init__(self, seq, struct=(0,2,4), stepsPerOctave=7):

        # 1. Try just adding seq and struct

        try:

            self.data = P(seq + struct)

        except:

            self.data = seq
            self.make()

            struct = Base.PGroup(struct)

            chords = []
            
            for item in self.data:
                val = (struct + item) % stepsPerOctave
                chords.append(val.sorted())

            self.data = chords

Pchords = PChords #: Alias

#### ---- Testing


#### -------------- These need updating

def irange(start, stop=None, step=0.1):
    r = []
    if not stop:
        stop = start
        start = 0
    while start <= stop:
        r.append( start )
        start += step
    return r

def Chord(stream=[0], structure=[0,2,4]):

    new = []

    for item in stream:

        new.append([item + s for s in structure])

    return new




def fShuf(a, b=None, size=8):

    if b:

        L = [a + (n * ( (b-a) / float(size))) for n in range(size)]

    else:

        L = [n * ( a / float(size)) for n in range(size)]

    random.shuffle(L)

    return L




def Walk(hi=8, variation=1, size=256):

    stream = [0]

    variation = 1.0 / variation

    step = random.choice([1,-1])

    while len(stream) < size:

        step = step * (-1)

        for x in range( int(hi * random.triangular(variation, 1)) - 1 ):

            stream.append( stream[-1] + step )

            if len(stream) == size:
                break

    return stream


def Sparse(arr=[0,1], hi=8):

    stream =[]

    return strema


def Geom(n, lo=1, hi=None):

    if not hi:

        hi = max(lo, 1)
        lo = min(lo, 1)

    return [n**i for i in range(lo, hi+1)]

def GeomFill(arr, N=2):
    """ GeomFill(arr) -> new_arr such that sum(new_list) is power of N """
    nums  = arr
    total = 1
    while sum(nums) >= total:
        total *= N
    nums.append( total - sum(nums) )
    return nums


def Rint(a, b=None):

    if b:

        return random.randrange(a, b)

    else:

        return random.randrange(0, a)


def Rhythm(string, step=0.5):

    stream = []

    dur = 0.0

    in_br = False

    for i, char in enumerate(string):

       # Needs work 

        if char == "[":

            in_br = True

            dur -= step

        elif char == "]":

            in_br = False

            dur -= step
        
        elif char != " ":

            stream.append(dur)

            dur = 0.0

        elif i == len(string) - 1:

            stream.append(dur + step)


        if in_br:

            dur += step/2.0

        else:   
    
            dur += step

    return stream[1:]





