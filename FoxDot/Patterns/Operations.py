from __future__ import division
from copy import copy
import Base

"""
    Module for key operations on Python lists or FoxDot Patterns
"""

class POperand:

    def __init__(self, func):
        
        self.operate = func

    def __call__(self, A, B):
        """ A is always a pattern.
        """

        # If the first pattern is empty, return empty

        if len(A) == 0:

            return A

        # Get the dominant pattern type and convert B

        cls = Base.Dominant(A, B)

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

        return cls(P1)

# General operations
Nil  = lambda a, b: a
Add  = lambda a, b: a + b
rAdd = lambda a, b: b + a
Sub  = lambda a, b: a - b
Mul  = lambda a, b: a * b
Div  = lambda a, b: a / b
Mod  = lambda a, b: a % b
rMod = lambda a, b: b % a
Pow  = lambda a, b: a ** b
rPow = lambda a, b: b ** a
rDiv = lambda a, b: b / a
rSub = lambda a, b: b - a
Get  = lambda a, b: a[b]
rGet = lambda a, b: b[a]

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




# --- Cases
#
#       [0,1] + 2 = [2,3]
#       (0,1) + 2 = (2,3)
#
#   [0,1] + [2,3] = [2,4]
#   [0,1] + (2,3) = [(2,3),(3,4)] -> [0,1] + [(2,3)] = [(2,3),(3,4)]
#
#   (0,1) + (2,3) = (2,4)
#   (0,1) + [2,3] = [(2,3),(3,4)]
#
#  [(0,1),2] + 3  = [(3,4),5]
#
#
#

#: Misc. Operations

def LCM(*args):
    """ Lowest Common Multiple """
    # Base case
    if len(args) == 1:
        return args[0]
    
    X = list(args)
    
    while any([X[0]!=K for K in X]):

        i = X.index(min(X))
        X[i] += args[i]        

    return X[0]

def patternclass(a, b):
    return Base.PGroup if isinstance(a, Base.PGroup) and isinstance(b, Base.PGroup) else Base.Pattern


def modi(array, i, debug=0):
    """ Returns the modulo index i.e. modi([0,1,2],4) will return 1 """
    try:
        return array[i % len(array)]
    except:        
        return array

def max_length(*patterns):
    """ Returns the largest length pattern """
    return max([len(p) for p in patterns])  


