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
        return "{" + self.data.string() + "}"

class PwRand(Main.GeneratorPattern):
    pass

class PxRand(Main.GeneratorPattern):
    pass

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
