from __future__ import absolute_import, division, print_function

from .Main import PGroup, PatternMethod
from ..Utils import modi

class PGroupPrime(PGroup):
    def change_state(self):
        """ To be overridden by any PGroupPrime that changes state after access by a Player """
        return
    def convert_data(self, *args, **kwargs):
        self.change_state()
        return PGroup.convert_data(self, *args, **kwargs)
    def has_behaviour(self):
        return True
    def calculate_step(self, dur):
        return float(dur) / len(self)
    def calculate_delay(self, delay):
        return delay

class PGroupStar(PGroupPrime):
    """ Stutters the values over the length of and event's 'dur' """    
    bracket_style="*()"
    def string(self):
        """ Used for SamplePlayerStrings """
        return "[" + PGroupPrime.string(self) + "]"

class PGroupPlus(PGroupPrime):
    """ Stutters the values over the length of and event's 'sus' """
    bracket_style="+()"
    def get_behaviour(self):
        def action(event, key):
            event['delay'] += self.calculate_time(float(event['sus']))
            return event
        return action

class PGroupPow(PGroupPrime):
    """ Stutters a shuffled version the values over the length of and event's 'dur' """
    bracket_style="**()"
    def calculate_time(self, dur):
        return PGroupPrime.calculate_time(self, dur).shuffle()    

class PGroupDiv(PGroupPrime):
    """ Stutter every other request """
    bracket_style="/()"
    counter = 0
    def __init__(self, *args, **kwargs):
        PGroupPrime.__init__(self, *args, **kwargs)
    def change_state(self):
        self.counter += 1
    def calculate_time(self, dur):
        if self.counter % 2 == 1:
            return PGroupPrime.calculate_time(self, dur)
        else:
            return 0

class PGroupMod(PGroupPlus):
    """ Useful for when you want many nested groups. This PGroup flattens the original
        but the delay times are calculated in the same way as if the values were neseted
     """
    bracket_style="%()"

    def __len__(self):
        return len([item for item in self])

    def getitem(self, index):
        return list(self)[index]

    def calculate_step(self, dur):
        return float(dur) / len(self.data)

    def calculate_time(self, dur):
        """ Returns a PGroup of durations to use as the delay argument
            when this is a sub-class of `PGroupPrime` """
        values = []
        step  = self.calculate_step(dur)
        for i, item in enumerate(self.data):
            delay = self.calculate_delay( i * step )
            if hasattr(item, "calculate_time"):
                delay += item.calculate_time( step )
            if isinstance(delay, PGroup):
                values.extend(list(delay))
            else:
                values.append( delay )
        return PGroup(values)

    def __iter__(self):
        return self.get_iter(self.data)

    @staticmethod
    def get_iter(group):
        """ Recursively unpacks nested PGroup into an un-nested group"""
        for item in group:
            if isinstance(item, PGroup):
                for sub in PGroupMod.get_iter(item.data):
                    yield sub
            else:
                yield item

#class PGroupFloorDiv(PGroupPrime):
#    """ Unused """
#    bracket_style="//()"

#class PGroupSub(PGroupPrime):
#    """ Unused """
#    bracket_style="-()"

class PGroupXor(PGroupPrime):
    """ The delay of this PGroup is s """
    bracket_style="^()"
    def __init__(self, *args):
        self.delay = 0
        PGroupPrime.__init__(self, *args)

    def set_delay(self, value):
        self.delay = value
        return self
    
    def calculate_step(self, dur):
        return self.delay

    def calculate_delay(self, delay):
        return delay



#class PGroupAnd(PGroupPrime):
#    """ Unused """
#    bracket_style="&()"
#    delay = 0
#    def __init__(self, args):
#        PGroupPrime.__init__(self, args[0])
#        if len(args) > 0:
#            self.delay = args[1]
#    def calculate_step(self, i, dur):
#        return i * self.delay

#class PGroupOr(PGroupPrime):
#    """ Unused """
#    bracket_style="|()"

# Define any pattern methods that use PGroupPrimes

@PatternMethod
def offadd(self, value, delay=0.5):
    return self + PGroupXor(0, value).set_delay(delay)

@PatternMethod
def offlayer(self, method, *args, **kwargs):
    """ Zips a pattern with a modified version of itself. Method argument
        can be a function that takes this pattern as its first argument,
        or the name of a Pattern method as a string. """
    
    if callable(method):
        func = method
        args = [self.data] + list(args)
    else:
        func = getattr(self, method)
        assert callable(func)

    delay = kwargs.get("dur", 0.5)

    return self.zip(func(*args, **kwargs), dtype=PGroupXor(0, value).set_delay(delay))
    
@PatternMethod
def amen(self, size=2):
    """ Merges and laces the first and last two items such that a
        drum pattern "x-o-" would become "(x[xo])-o([-o]-)" """
    new = []

    for n in range(len(self.data)):

        if  n % 4 == 0:

            new.append([self.data[n], PGroupPlus(self.data[n], modi(self.data, n + size))])

        elif n % 4 == 2:

            new.append( [self.data[n]]*3+[self.data[n-1]] )

        elif n % 4 == 3:

            new.append( [PGroupPlus(self.data[n], self.data[n-1]), [self.data[n], self.data[n-1]] ] )

        else:

            new.append(self.data[n])
    
    return self.__class__(new)
