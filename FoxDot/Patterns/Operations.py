from __future__ import division
import Base

"""
    Module for key operations on Python lists or FoxDot Patterns
"""

def modi(array, i, debug=0):
    """ Returns the modular index i.e. modi([0,1,2],4) will return 1 """
    try:
        return array[i % len(array)]
    except:        
        return array

def max_length(*patterns):
    """ Returns the largest length pattern """
    return max([len(p) for p in patterns])

#: The following return operand patterns

class POperand:

    def __init__(self, func):
        
        self.operate = func

    def __call__(self, A, B):

        # Trivial case

        if isinstance(B, (int, float)):

            return A.__class__([self.operate(a, B) for a in A])

        # Multiple patterns

        pat1, pat2 = self.setup(A, B)

        for i, item in pat1.items():

            try:

                # Perform the operation

                pat1[i] = self.operate(item, pat2[i])

            except ZeroDivisionError:

                # Numbers divided by 0 are set to 0

                pat1[i] = 0

        return pat1

    @staticmethod
    def setup(A, B):
        """ Prepares two Patterns, A & B, for correct use in operands"""
        try:
            A = A.copy() # Make a copy of A
        except:
            pass

        A, B = Base.Convert(A, B)
        
        # If at least one is a 'true' pattern, convert the other
        if isinstance(A, Base.Pattern):
            B = Base.asStream(B)
        elif isinstance(B, Base.Pattern):
            A = Base.asStream(A)

        # If we have two 

        Length = max_length(A, B)

        A.stretch(Length)
        B.stretch(Length)
        
        return A, B

# General operations
Nil  = lambda a, b: a
Add  = lambda a, b: a + b
Sub  = lambda a, b: a - b
Mul  = lambda a, b: a * b
Div  = lambda a, b: a / b
Mod  = lambda a, b: a % b
Pow  = lambda a, b: a ** b
rDiv = lambda a, b: b / a
rSub = lambda a, b: b - a

# Pattern operations
PAdd = POperand(Add)
PSub = POperand(Sub)
PMul = POperand(Mul)
PDiv = POperand(Div)
PMod = POperand(Mod)
PPow = POperand(Pow) # a ^ b also calls this



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
#


