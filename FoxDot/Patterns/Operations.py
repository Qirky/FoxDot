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
        self.call = self.__call__

    def __call__(self, A, B):

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

        if not isinstance(A, Base.Pattern):
            A = Base.Pattern(A)
        if not isinstance(B, Base.Pattern):
            B = Base.Pattern(B)
            
        Length = max_length(A, B)

        A.stretch(Length)
        B.stretch(Length)

        #: If B is a PGroup, A is returned as a PGroup
        if isinstance(B, Base.PGroup):
            A = Base.PGroup(A)

        return A, B


PAdd = POperand(lambda a, b: a + b)
PSub = POperand(lambda a, b: a - b)
PMul = POperand(lambda a, b: a * b)
PDiv = POperand(lambda a, b: a / b)
PMod = POperand(lambda a, b: a % b)
PPow = POperand(lambda a, b: a ** b) # a ^ b also calls this




