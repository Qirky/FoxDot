""" Utility functions for Pattern types """

import functools
import inspect
import Main

def loop_pattern_func(f):
    ''' Decorator for allowing any Pattern function to create
        multiple Patterns by using Patterns as arguments '''
    @functools.wraps(f)
    def new_function(*args):
        pat = Main.Pattern()
        for i in range(LCM(*[len(arg) for arg in args if (hasattr(arg, '__len__') and not isinstance(arg, Main.PGroup))])):
            pat |= f(*[(modi(arg, i) if not isinstance(arg, Main.PGroup) else arg) for arg in args])
        return pat
    new_function.argspec = inspect.getargspec(f)
    return new_function

def loop_pattern_method(f):
    ''' Decorator for allowing any Pattern method to create
        multiple (or rather, longer) Patterns by using Patterns as arguments '''
    @functools.wraps(f)
    def new_function(self, *args):
        pat = Main.Pattern()
        for i in range(LCM(*[len(arg) for arg in args if (hasattr(arg, '__len__') and not isinstance(arg, Main.PGroup))])):
            pat |= f(self, *[(modi(arg, i) if not isinstance(arg, Main.PGroup) else arg) for arg in args])
        return pat
    new_function.argspec = inspect.getargspec(f)
    return new_function

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

def pattern_depth(pat):
    """ Returns the level of nested arrays """	
    total = 1
    for item in pat:
        if isinstance(item, Main.PGroup):
            depth = pattern_depth(item)
            if depth + 1 > total:
                total = depth + 1
    return total

def group_modi(pgroup, index):
    """ Returns value from pgroup that modular indexes nested groups """
    if isinstance(pgroup, (int, float, str, bool)):
        return pgroup
    try:
        sub_index = index // len(pgroup)
        mod_index = int(sub_index / pattern_depth(pgroup))
        return group_modi(pgroup[index % len(pgroup)], mod_index)
    except(TypeError, AttributeError, ZeroDivisionError):
        return pgroup

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
