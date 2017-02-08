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
import math
from Base import Pattern, GeneratorPattern, PGroup, asStream
from Operations import *

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
        if hasattr(args, '__iter__'):
            data = []
            for item in args:
                if type(item) is slice:
                    data.extend(sliceToRange(item))
                else:
                    data.append(item)
        elif type(args) is slice:
            data = sliceToRange(args)
        else:
            data = args
        return Pattern(data)
    
    def __call__(self, *args):
        return PGroup(args if len(args) > 1 else args[0])

# This is a pattern creator  
P = __pattern__()

#================================#
#      2. Pattern Functions      #
#================================#

#: Pattern functions that take patterns as arguments

def PStutter(seq, n=2):
    """ PStutter(seq, n) -> Creates a pattern such that each item in the array is repeated n times (n can be a pattern) """
    return Pattern(seq).stutter(n)

def PShuf(seq):
    ''' PShuf(seq) -> Returns a shuffled version of seq'''
    return Pattern(seq).shuffle()

def PAlt(pat1, pat2, *patN):
    data = []
    item = [asStream(p) for p in [pat1, pat2] + list(patN)]
    size = LCM(*[len(i) for i in item])
    for n in range(size):
        for i in item:
            data.append(modi(i,n))
    return Pattern(data)

def PStretch(seq, size):
    return Pattern(data).stretch(size)

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
        p.append(P[pat])
        l.append(len(p[-1]))
    length = LCM(*l)
    return Pattern([tuple(pat[i] for pat in p) for i in range(length)])


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

#: Pattern functions that take single values

def loop_pattern_func(f):
    ''' Wrapper for allowing any Pattern function to create
        multiple Patterns by using Patterns as arguments '''
    def new_function(*args):
        pat = Pattern()
        for i in range(LCM(*[len(arg) for arg in args if hasattr(arg, '__len__')])):
            pat |= f(*[modi(arg, i) for arg in args])
        return pat
    return new_function

@loop_pattern_func
def PSq(a=1, b=2, c=3):
    return Pattern([x**b for x in range(a,a+c)])

@loop_pattern_func
def P10(n):
    return Pattern([random.choice((0,1)) for i in range(int(n))])

@loop_pattern_func
def PStep(n, value, default=0):
    return Pattern([default] * (n-1) + [value])

@loop_pattern_func
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

@loop_pattern_func
def PRange(start, stop=None, step=None):        
    return Pattern(range(*[val for val in (start, stop, step) if val is not None]))

@loop_pattern_func
def PTri(start, stop=None, step=None):
    rev_step = step if step is not None else 1
    data = list(PRange(start, stop, step))
    return Pattern(data + [item + rev_step for item in reversed(data)])

@loop_pattern_func
def PSine(n=16):
    """ Returns values of one cycle of sine wave split into 'n' parts """
    i = (2 * math.pi) / n
    return Pattern([math.sin(i * j) for j in range(int(n))])

@loop_pattern_func
def PEuclid(n, k):
    ''' Returns the Euclidean rhythm which spreads 'n' pulses over 'k' steps as evenly as possible.
        e.g. PEuclid(3, 8) -> P[1, 0, 0, 1, 0, 0, 1, 0] '''
    return Pattern( EuclidsAlgorithm(n, k) )

@loop_pattern_func
def PDur(n, k, dur=0.25):
    """ Returns the *actual* durations based on Euclidean rhythms (see PEuclid) where dur
        is the length of each step.
        e.g. PDur(3, 8) -> P[0.75, 0.75, 0.5] """

    data = EuclidsAlgorithm(n, k)

    count, seq = 1, []

    for item in data[1:]:
        if item == 1:
            seq.append(count)
            count = 1
        else:
            count += 1

    seq.append(count)       

    return Pattern(seq) * dur

#==============================#
#      2. Generator Types      #
#==============================#

class __generatorpattern__:
    ''' Pseudo-RandomGenerator.
        R[1,2,3]
    '''
    def __getitem__(self, args):
        return PRand(list(args) if hasattr(args, '__iter__') else args)
        
R = __generatorpattern__()

class PRand(GeneratorPattern):
    def __init__(self, start, stop=None):
        GeneratorPattern.__init__(self)
        if hasattr(start, "__iter__"):
            self.data = Pattern(start)
            self.func = lambda index: random.choice(self.data)
        else:
            self.low  = start if stop is not None else 0
            self.high = stop  if stop is not None else start
    def func(self, index):
        return random.randrange(self.low, self.high)

#TODO
class PwRand(GeneratorPattern):
    pass

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
