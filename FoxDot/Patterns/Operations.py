import Base

"""
    Module for key operations on Python lists or FoxDot Patterns
"""

def modi(array, i):
    """ Returns the modular index i.e. modi([0,1,2],4) will return 1 """
    try:
        return array[i % len(array)]
    except:
        return array

def max_length(*patterns):
    """ Returns the largest length pattern """
    return max([len(p) for p in patterns])

#: The following return operand patterns

def POperand(A, B):
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

def PAdd(A, B):
    """ Returns the vector addition of A and B """

    pat1, pat2 = POperand(A, B)

    for i, item in pat1.items():

        pat1[i] = item + pat2[i]            
    
    return pat1

def PSub(A, B):
    """ Returns the vector subraction of B from A """

    pat1, pat2 = POperand(A, B)

    for i, item in pat1.items():

        pat1[i] = item - pat2[i]            
    
    return pat1
    

def PMul(A, B):
    """ Returns the array calculated by multiplying each value in A by the corresponding value in B """

    pat1, pat2 = POperand(A, B)

    for i, item in pat1.items():

        pat1[i] = item * pat2[i]
    
    return pat1

def PDiv(A, B):
    """ Returns the array calculated by multiplying each value in A by the corresponding value in B """
    pat1, pat2 = POperand(A, B)

    for i, item in pat1.items():    

        try:

            pat1[i] = float(item) / pat2[i]

        except:

            pat1[i] = item / pat2[i]
    
    return pat1
