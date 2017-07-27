"""

    Useful functions and classes, mostly relating to the Pattern class
    but used in multiple sub-packages of FoxDot.

"""

from __future__ import absolute_import, division, print_function

import sys

# Functions

def stdout(*args):
    """ Forces prints to stdout and not console """
    sys.__stdout__.write(" ".join([str(s) for s in args]) + "\n")

def sliceToRange(s):
    start = s.start if s.start is not None else 0
    stop  = s.stop 
    step  = s.step if s.step is not None else 1
    try:
        return list(range(start, stop, step))
    except OverflowError:
        raise TypeError("range() integer end argument expected, got NoneType")

def LCM(*args):
    """ Lowest Common Multiple """

    args = [n for n in args if n != 0]
    
    # Base case
    if len(args) == 0:
        return 1
    
    elif len(args) == 1:
        return args[0]

    X = list(args)
    
    while any([X[0]!=K for K in X]):

        i = X.index(min(X))
        X[i] += args[i]        

    return X[0]

def EuclidsAlgorithm(n, k):
    
    if n == 0: return [n for i in range(k)]
    
    data = [[1 if i < n else 0] for i in range(k)]
    
    while True:
        
        k = k - n

        if k <= 1:
            break

        elif k < n:
            n, k = k, n

        for i in range(n):
            data[i] += data[-1]
            del data[-1]
    
    return [x for y in data for x in y]


def modi(array, i, debug=0):
    """ Returns the modulo index i.e. modi([0,1,2],4) will return 1 """
    try:
        return array[i % len(array)]
    except(TypeError, AttributeError, ZeroDivisionError): 
        return array

def get_expanded_len(data):
    """ (0,(0,2)) returns 4. int returns 1 """
    if type(data) is str and len(data) == 1:
        return 1
    l = []
    try:
        for item in data:
            try:
                l.append(get_expanded_len(item))
            except(TypeError, AttributeError):
                l.append(1)
        return LCM(*l) * len(data)
    except TypeError:
        return 1

def max_length(*patterns):
    """ Returns the largest length pattern """
    return max([len(p) for p in patterns])  

# Classes

class dots:        
    """ Class for representing long Patterns in strings """
    def __repr__(self):
        return '...'
