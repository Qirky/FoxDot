import random

# Circular add and get

def modi(array, i):
    """ Returns the modular index i.e. modi([0,1,2],4) will return 1 """
    try:
        return array[i % len(array)]
    except:
        return array

def circular_add(a, b):
    """ Adding contents of b to a """
    if len(b) > len(a):
        tmp = b
        b = a
        a =tmp
        
    tmp = []
    
    for i in range(len(a)):

        tmp.append( float(a[i]) + float(b[i % len(b)]) )

    return tmp

def GreedyZip(a, b):
    """ Greedy version of zip """
    exp = max(len(a), len(b))
    
    a = Stretch(a, exp)
    b = Stretch(b, exp)

    return zip(a, b)

# Define python functions that can be used in the live code

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
        

def Place(stream):
    """ nested streams are stretched
        e.g. [[1,0],0,1,0] would be returned as [1,0,1,0,0,0,1,0] """

    # If no nested values, return original stream

    try:

        largest_sub = max([len(a) for a in stream if type(a) == list])

    except:

        return stream

    new_stream = []

    for i in range( largest_sub ):

        for j in range(len(stream)):

            item = stream[j]

            if type(item) == list:

                item = item[i % len(item)]

            new_stream.append(item)
    
    return new_stream

def Stutter(stream, n):

    if type(n) == int:

        n = [n for i in stream]

    new_stream = []

    for i, item in enumerate(stream):

        for j in range(n[i]):

            new_stream.append( item )

    return new_stream 

def Shuf(a, b=None, size=None):

    if type(a) == list:

        random.shuffle(a)

        return a

    try:
        if not size:
            size = b - a
    except:
        if not size:
            size = a
            
    return [random.randrange(a, b) for i in range(size)]


def fShuf(a, b=None, size=8):

    if b:

        L = [a + (n * ( (b-a) / float(size))) for n in range(size)]

    else:

        L = [n * ( a / float(size)) for n in range(size)]

    random.shuffle(L)

    return L

def White(lo=0, hi=1, size=256):

    lo = float(lo)
    hi = float(hi)

    mode = (lo + hi) / 2.0

    L = [random.triangular(lo, hi, mode) for n in range(size)]

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

def Rand(a, b=None, size=256):

    if type(a) == list:

        return [random.choice(a) for n in range(size)]

    else:

        return [random.randrange(a, b) for n in range(size)]

def Rint(a, b=None):

    if b:

        return random.randrange(a, b)

    else:

        return random.randrange(0, a)



def Sine(size=16):

    a = [-1.0 + (2*n)/float(size / 2) for n in range(size)]
    b = [ 1.0 - (2*n)/float(size / 2) for n in range(size)]

    return a + b

def Stretch(stream, size):
    out = []
    for n in range(size):
        out.append( modi(stream, n) )
    return out

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

# Used for converting streams and frequencies

def miditofreq(midinote):
    """ Converts a midi number to frequency """
    return 440 * (2 ** ((midinote - 69.0)/12.0))

def midi(scale, octave, degree, root=0, stepsPerOctave=12):

    lo = int(degree)
    hi = lo + 1

    octave = octave + (lo / len(scale))

    chroma = range(stepsPerOctave)

    scale_val = (scale[hi % len(scale)] - scale[lo % len(scale)]) * ((degree-lo)) + scale[lo % len(scale)]

    return scale_val + (octave * len(chroma)) + chroma[ root % len(chroma) ]

# These patterns take Player objects as arguments, change their state, and return None

def rev(player):
    player.reverse()

def lshift(player):
    player.lshift()

def rshift(player):
    player.rshift()

def shuf(player):
    player.degree = Shuf(player.degree)


