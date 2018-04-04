from __future__ import absolute_import, division, print_function

from ..Utils import *

"""
    Module for key operations on Python lists or FoxDot Patterns
"""

# PATTERN_WEIGHTS = ["Pattern", "PGroupPrime", "PGroup", "metaPGroupPrime"]

def old_DominantPattern(*patterns):
    """ Returns the class (and the relative pattern) for the
        type of Pattern to use in a mathematical operation """
    classes =  [p.__class__.__name__ for p in patterns]
    print(classes, PATTERN_WEIGHTS)
    for i, name in enumerate(PATTERN_WEIGHTS):
        if name in classes:
            break
    pat = patterns[classes.index(name)]
    cls = pat.__class__    
    return cls, pat    

def DominantPattern(*patterns):    
    return min([p for p in patterns if hasattr(p, "WEIGHT")], key = lambda x: x.WEIGHT)


class POperand:

    def __init__(self, func):
        
        self.operate = func

    def __call__(self, A, B):
        """ A is always a Pattern or PGroup."""

        # If the first pattern is empty, return the other as a pattern

        if len(A) == 0:

            return A.__class__(B)

        # Get the dominant pattern type and convert B

        key = DominantPattern(A, B)

        cls = key.__class__

        # Instead of coverting the dominant to its own class, make a true_copy?

        A = cls(A)
        B = cls(B)

        # Calculate total length before operations

        i, length = 0, LCM(len(A.data), len(B.data))

        P1 = []

        while i < length:

            try:

                try:

                    val = self.operate(modi(A.data, i), modi(B.data, i))

                except TypeError as e:

                    raise TypeError("Cannot operate on {!r} and {!r}".format(A, B))

            except ZeroDivisionError:

                val = 0

            P1.append(val)
            i += 1

        # Copy the dominant pattern and set the new data vals

        return key.true_copy(P1)

# General operations
def Nil(a, b):  return a
def Add(a, b):  return a + b
def Sub(a, b):  return a - b
def Mul(a, b):  return a * b
def Div(a, b):  return a / b
def Mod(a, b):  return a % b
def Pow(a, b):  return a ** b
def Get(a, b):  
    try: 
        return a[b]
    except TypeError: 
        return a
def FloorDiv(a, b): return a // b
def Xor(a, b): return a ^ b
def Or(a, b):  return a | b

def rAdd(a, b): return b + a
def rGet(a, b):  
    try: 
        return b[a]
    except TypeError: 
        return b
def rSub(a, b): return b - a
def rMul(a, b): return b * a
def rDiv(a, b): return b / a
def rMod(a, b): return b % a
def rPow(a, b): return b ** a
def rFloorDiv(a, b): return b // a
def rXor(a, b): return b ^ a
def rOr(a, b):  return b | a

# Pattern operations
PAdd = POperand(Add)

PSub = POperand(Sub)
PSub2 = POperand(rSub)

PMul = POperand(Mul)

PDiv = POperand(Div)
PDiv2 = POperand(rDiv)

PFloor = POperand(FloorDiv)
PFloor2 = POperand(rFloorDiv)

PMod = POperand(Mod)
PMod2 = POperand(rMod)

PPow = POperand(Pow)
PPow2 = POperand(rPow)

PGet = POperand(Get)

# Pattern comparisons -> need to maybe have a equals func?
PEq = lambda a, b: (all([int(a[i]==b[i]) for i in range(len(a))]) if len(a) == len(b) else False) if a.__class__ == b.__class__ else False
PNe = lambda a, b: (any([int(a[i]!=b[i]) for i in range(len(a))]) if len(a) == len(b) else True) if a.__class__ == b.__class__ else True