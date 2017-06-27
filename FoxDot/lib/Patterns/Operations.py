from __future__ import division
from utils import *
import Main
import PlayString

"""
    Module for key operations on Python lists or FoxDot Patterns
"""

class POperand:

    def __init__(self, func):
        
        self.operate = func

    def __call__(self, A, B):
        """ A is always a Pattern or PGroup.
        """

        # If the first pattern is empty, return the other as a pattern

        if len(A) == 0:

            return Main.Pattern(B)

        # Get the dominant pattern type and convert B

        cls, key = Main.Dominant(A, B)

        # Instead of coverting the dominant to its own class, make a true_copy
        
        A = cls(A)
        B = cls(B)

        # Calculate total length before operations

        i, length = 0, LCM(len(A), len(B))

        P1 = []

        while i < length:

            try:

                val = self.operate(A[i], B[i])

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
def Get(a, b):  return a[b]
def FloorDiv(a, b): return a // b

def rAdd(a, b): return b + a
def rGet(a, b): return b[a]
def rSub(a, b): return b - a
def rDiv(a, b): return b / a
def rMod(a, b): return b % a
def rPow(a, b): return b ** a
def rFloorDiv(a, b): return b // a

# Pattern operations
PAdd = POperand(Add)

PSub = POperand(Sub)
PSub2 = POperand(rSub)

PMul = POperand(Mul)

PDiv = POperand(Div)
PDiv2 = POperand(rDiv)

PMod = POperand(Mod)
PMod2 = POperand(rMod)

PPow = POperand(Pow)
PPow2 = POperand(rPow)

PGet = POperand(Get)

# Pattern comparisons -> need to maybe have a equals func?
PEq = lambda a, b: (all([a[i]==b[i] for i in range(len(a))]) if len(a) == len(b) else False) if a.__class__ == b.__class__ else False
PNe = lambda a, b: (any([a[i]!=b[i] for i in range(len(a))]) if len(a) == len(b) else True) if a.__class__ == b.__class__ else True
