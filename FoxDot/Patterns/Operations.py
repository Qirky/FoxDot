from __future__ import division
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

        # If the first pattern is empty, return the other as a pattern

        if len(A) == 0:

            return Base.Pattern(B)

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
def Nil(a, b):  return a
def Add(a, b):  return a + b
def Sub(a, b):  return a - b
def Mul(a, b):  return a * b
def Div(a, b):  return a / b
def Mod(a, b):  return a % b
def Pow(a, b):  return a ** b
def Get(a, b):  return a[b]

def rAdd(a, b): return b + a
def rGet(a, b): return b[a]
def rSub(a, b): return b - a
def rDiv(a, b): return b / a
def rMod(a, b): return b % a
def rPow(a, b): return b ** a

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


