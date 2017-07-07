"""
    Generator patterns are similar to Pattern objects but instead of being
    a set of values, they return a value when accessed / indexed based on
    a function.

"""

import Main

# Random Generator Pattern

import random

class PRand(Main.GeneratorPattern):
    ''' Returns a random integer between start and stop. If start is a container-type it returns
        a random item for that container. '''
    def __init__(self, start, stop=None):
        Main.GeneratorPattern.__init__(self)
        if hasattr(start, "__iter__"):
            self.data = Main.Pattern(start)
            def choose(index):
                return random.choice(self.data)
            self.func = choose
            self.low = self.high = None
        else:
            self.low  = start if stop is not None else 0
            self.high = stop  if stop is not None else start
            self.data = "{}, {}".format(self.low, self.high)
    def func(self, index):
        return random.randrange(self.low, self.high)
    def string(self):
        """ Used in PlayString to show a PRand in curly braces """
        return "{" + self.data.string() + "}"

class PTree(Main.GeneratorPattern):
    """ Takes a starting value and two functions as arguments. The first function, f, must
        take one value and return a container-type of values and the second function, choose,
        must take a container-type and return a single value. In essence you are creating a
        tree based on the f(n) where n is the last value chosen by choose.
    """
    def __init__(self, n=0, f=lambda x: (x + 1, x - 1), choose=lambda x: random.choice(x)):
        Main.GeneratorPattern.__init__(self)
        self.f  = f
        self.choose = choose
        self.values = [n]

    def func(self, index):
        self.values.append( self.choose(self.f( self.values[-1] )) )
        return self.value
        
        

class PwRand(Main.GeneratorPattern):
    pass

class PxRand(Main.GeneratorPattern):
    pass

class PWalk(Main.GeneratorPattern):
    def __init__(self, max=7, step=1, start=0):

        Main.GeneratorPattern.__init__(self)
        
        self.max   = abs(max)
        self.min   = self.max * -1
        
        self.step  = Main.asStream(step).abs()
        self.start = start

        self.data = [self.start, self.step, self.max]

        self.directions = [lambda x, y: x + y, lambda x, y: x - y]

        self.last_value = None

    def func(self, index):
        if self.last_value is None:
            self.last_value = 0
        else:
            if self.last_value >= self.max: # force subtraction
                f = self.directions[1]
            elif self.last_value <= self.min: # force addition
                f = self.directions[0]
            else:
                f = random.choice(self.directions)
            self.last_value = f(self.last_value, self.step.choose())
        return self.last_value

            
        

class PWhite(Main.GeneratorPattern):
    ''' Returns random floating point values between 'lo' and 'hi' '''
    def __init__(self, lo=0, hi=1):
        Main.GeneratorPattern.__init__(self)
        self.low = float(lo)
        self.high = float(hi)
        self.mid = (lo + hi) / 2.0
        self.data = "{}, {}".format(self.low, self.high)
    def func(self, index):
        return random.triangular(self.low, self.high, self.mid)

class PSquare(Main.GeneratorPattern):
    ''' Returns the square of the index being accessed '''
    def func(self, index):
        return index * index
