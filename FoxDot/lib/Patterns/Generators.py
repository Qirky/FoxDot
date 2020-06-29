"""

    This module contains all the sub-classes of `GeneratorPattern` used in FoxDot. Unlike
    a `Pattern`, a `GeneratorPattern` does not contain a list that is iterated over or
    indexed but returns a value based on the index and an internal function. For example,
    `PRand` returns a random value from a list of values. It will always return the same
    value for the same index as it stores this in its internal cache. `Pattern` methods
    such as `rotate` or `palindrome` are not available from the `GeneratorPattern` class
    but slicing generators will return a `Pattern` object from which these methods can
    be called e.g.

        >>> gen = PRand([0,1,2])
        >>> pat = gen[:5]
        P[0, 1, 0, 2, 1]
        >>> pat.rotate()
        P[1, 0, 2, 1, 0]

    Mathematical operations *do* work in the same way as they do in `Patterns`.

        >>> gen1 = PRand([0,1,2])
        >>> gen2 = gen1 + 10
        >>> gen1[:5]
        P[0, 2, 2, 1, 0]
        >>> gen2[:5]
        P[10, 12, 12, 11, 10]

"""


from __future__ import absolute_import, division, print_function

from .Main  import GeneratorPattern, Pattern, asStream, PatternInput

import random

class RandomGenerator(GeneratorPattern):
    __seed = None
    def __init__(self, *args, **kwargs):
        GeneratorPattern.__init__(self, *args, **kwargs)
        self.random = random

    def init_random(self, *args, **kwargs):
        """ To be called at the end of the __init__ """

        if "seed" in kwargs:
            self.random = self.random.Random()
            self.random.seed(kwargs["seed"])
        
        elif RandomGenerator.__seed is not None:
            self.random = self.random.Random()
            self.random.seed(RandomGenerator.__seed)

            pattern = self[:5000]

            self.__class__ = Pattern
            self.data = pattern.data

        return self

    @classmethod
    def set_override_seed(cls, seed):
        cls.__seed = seed
        return

    # Pseudo-inheritance
    def choice(self, *args, **kwargs):
        return self.random.choice(*args, **kwargs)

    def randint(self, *args, **kwargs):
        return self.random.randint(*args, **kwargs)

    def triangular(self, *args, **kwargs):
        return self.random.triangular(*args, **kwargs)

class PRand(RandomGenerator):
    ''' Returns a random integer between start and stop. If start is a container-type it returns
        a random item for that container. '''
    def __init__(self, start, stop=None, **kwargs):
        # If we're given a list, choose from that list -- TODO always use a list and use range
        RandomGenerator.__init__(self, **kwargs)

        self.args = (start, stop)
        self.kwargs = kwargs
        
        # Choosing from a list
        if hasattr(start, "__iter__"):
            self.data = Pattern(start)
            try:
                assert(len(self.data)>0)
            except AssertionError:
                raise AssertionError("{}: Argument size must be greater than 0".format(self.name))
            self.choosing = True
            self.low = self.high = None
        
        else:
            # Choosing from a range
            self.choosing = False
            self.low  = start if stop is not None else 0
            self.high = stop  if stop is not None else start
            try:
                assert((self.high - self.low)>=1)
            except AssertionError:
                raise AssertionError("{}: Range size must be greater than 1".format(self.name))
            self.data = "{}, {}".format(self.low, self.high)

        self.init_random(**kwargs)

    def choose(self):
        return self.data[self.choice(range(self.MAX_SIZE))]
            
    def func(self, index):
        if self.choosing:
            # value = self.choice(self.data)
            value = self.choose()
        else:
            value = self.randint(self.low, self.high)
        return value

    def string(self):
        """ Used in PlayString to show a PRand in curly braces """
        return "{" + self.data.string() + "}"

class PWhite(RandomGenerator):
    ''' Returns random floating point values between 'lo' and 'hi' '''
    def __init__(self, lo=0, hi=1, **kwargs):
        RandomGenerator.__init__(self, **kwargs)
        self.args = (lo, hi)
        self.low = float(lo)
        self.high = float(hi)
        self.mid = (lo + hi) / 2.0
        self.data = "{}, {}".format(self.low, self.high)
        self.init_random(**kwargs)

    def func(self, index):
        return self.triangular(self.low, self.high, self.mid)

class PxRand(PRand):
    def func(self, index):
        value = PRand.func(self, index)
        while value == self.last_value:
            value = PRand.func(self, index)
        self.last_value = value                
        return self.last_value

class PwRand(RandomGenerator):
    def __init__(self, values, weights, **kwargs):
        RandomGenerator.__init__(self, **kwargs)

        self.args = (values, weights)
        
        try:
            assert(all(type(x) == int for x in weights))
        except AssertionError:
            e = "{}: Weights must be integers".format(self.name)
            raise AssertionError(e)
        
        self.data    = Pattern(values)
        self.weights = Pattern(weights).stretch(len(self.data))
        self.values  = self.data.stutter(self.weights)
        
        self.init_random(**kwargs)

    def choose(self):
        return self.values[self.choice(range(self.MAX_SIZE))]
        
    def func(self, index):
        return self.choose()

class PChain(RandomGenerator):
    """ An example of a Markov Chain generator pattern. The mapping argument 
        should be a dictionary of keys whose values are a list/pattern of possible
        destinations.  """
    def __init__(self, mapping, **kwargs):

        assert isinstance(mapping, dict)

        RandomGenerator.__init__(self, **kwargs)
        
        self.args = (mapping,)

        self.last_value = 0
        self.mapping = {}
        i = 0
        for key, value in mapping.items():
            self.mapping[key] = self._convert_to_list(value)
            # Use the first key to start with
            if i == 0:
                self.last_value = key
                i += 1

        self.init_random(**kwargs)
                
    def func(self, *args, **kwargs):
        index = self.last_value
        if isinstance(self.last_value, GeneratorPattern):
            index = index.CACHE_HEAD
        if index in self.mapping:
            self.last_value = self.choice(self.mapping[index])
        return self.last_value

    def _convert_to_list(self, value):
        if isinstance(value, list):
            return value
        elif isinstance(value, Pattern):
            return value.data
        return [value]

class PZ12(GeneratorPattern):
    """ Implementation of the PZ12 algorithm for predetermined random numbers. Using
        an irrational value for p, however, results in a non-determined order of values. 
        Experimental, only works with 2 values.
    """
    def __init__(self, tokens=[1,0], p=[1, 0.5]):
        GeneratorPattern.__init__(self)
        self.data    = tokens
        self.probs = [value / max(p) for value in p]
        self._prev   = []
        self.dearth  = [0 for n in self.data]

    def _count_values(self, token):    
        return sum([self._prev[i] == token for i in range(len(self._prev))])

    def func(self, index):
        index = len(self._prev)
        for i, token in enumerate(self.data):
            d0 = self.probs[i] * (index + 1)
            d1 = self._count_values(token)
            self.dearth[i] = d0-d1
        i = self.dearth.index(max(self.dearth))
        value = self.data[i]
        self._prev.append(value)
        return value

class PTree(RandomGenerator):
    """ Takes a starting value and two functions as arguments. The first function, f, must
        take one value and return a container-type of values and the second function, choose,
        must take a container-type and return a single value. In essence you are creating a
        tree based on the f(n) where n is the last value chosen by choose.
    """
    def __init__(self, n=0, f=lambda x: (x + 1, x - 1), choose=lambda x: random.choice(x), **kwargs):

        RandomGenerator.__init__(self, **kwargs)
                
        self.args=(n, f, choose)

        self.f  = f
        self.choose = choose
        self.values = [n]

        self.init_random(**kwargs)

    def func(self, index):
        self.values.append( self.choose(self.f( self.values[-1] )) )
        return self.values[-1]

class PWalk(RandomGenerator):
    def __init__(self, max=7, step=1, start=0, **kwargs):

        RandomGenerator.__init__(self, **kwargs)

        self.args = (max, step, start)
        
        self.max   = abs(max)
        self.min   = self.max * -1
        
        self.step = PatternInput(step).transform(abs)
        self.start = start

        self.data = [self.start, self.step, self.max]

        self.directions = [lambda x, y: x + y, lambda x, y: x - y]

        self.last_value = None

        self.init_random(**kwargs)

    def func(self, index):
        if self.last_value is None:
            self.last_value = self.start
        else:
            if self.last_value >= self.max: # force subtraction
                f = self.directions[1]
            elif self.last_value <= self.min: # force addition
                f = self.directions[0]
            else:
                f = self.choice(self.directions)
            self.last_value = f(self.last_value, self.step[index])
        return self.last_value


class PDelta(GeneratorPattern):
    def __init__(self, deltas, start=0):
        GeneratorPattern.__init__(self)
        self.deltas = asStream(deltas)
        self.start  = start
        self.value  = start
    def func(self, index):  
        if index == 0:
            return self.start
        self.value += float(self.deltas[index - 1])
        return self.value
        
class PSquare(GeneratorPattern):
    ''' Returns the square of the index being accessed '''
    def func(self, index):
        return index * index

class PIndex(GeneratorPattern):
    ''' Returns the index being accessed '''
    def func(self, index):
        return index

class PFibMod(GeneratorPattern):
    """ Returns the fibonacci sequence -- maybe a bad idea"""
    def func(self, index):
        if index < 2: return index
        a = self.cache.get(index-1, self.getitem(index-1))
        b = self.cache.get(index-2, self.getitem(index-2))
        return a + b
