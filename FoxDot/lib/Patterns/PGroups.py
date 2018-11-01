from __future__ import absolute_import, division, print_function

from .Main import PGroup, PatternMethod, GeneratorPattern, sum_delays
from ..Utils import modi, LCM

class PGroupPrime(PGroup):
    WEIGHT  = 1
    """ Base class for PGroups with "behavior" that affect a Player's event dictionary """
    def change_state(self):
        """ To be overridden by any PGroupPrime that changes state after access by a Player """
        return
    def convert_data(self, *args, **kwargs):
        self.change_state()
        return PGroup.convert_data(self, *args, **kwargs)
    def has_behaviour(self):
        return True
    def _get_step(self, dur):
        return float(dur) / len(self)
    def _get_delay(self, delay):
        return delay

class metaPGroupPrime(PGroupPrime):
    """ Base class for PGroups that take any extra arguments to be stored """
    WEIGHT = 3
    def __init__(self, *args, **kwargs):
        PGroupPrime.__init__(self, *args, **kwargs)
        if isinstance(self, PGroup):
            self.meta = self.data[self.ignore:]
            self.data = self.data[:self.ignore]

class PGroupStar(PGroupPrime):
    """ Stutters the values over the length of and event's 'dur' """    
    bracket_style="*()"

class PGroupPlus(PGroupPrime):
    """ Stutters the values over the length of and event's 'sus' """
    bracket_style="+()"
    def get_behaviour(self):
        """ Returns a function that modulates a player event dictionary """
        def action(event, key):
            this_delay = self.calculate_time(float(event['sus']))
            return self._update_event(event, key, this_delay)
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
    """ OBSOLETE
        --------
        Useful for when you want many nested groups. This PGroup flattens the original
        but the delay times are calculated in the same way as if the values were neseted
     """
    bracket_style="%()"

    def __len__(self):
        return len([item for item in self])

    def getitem(self, index):
        return list(self)[index]

    def _get_step(self, dur):
        return float(dur) / len(self.data)

    def calculate_time(self, dur):
        """ Returns a PGroup of durations to use as the delay argument
            when this is a sub-class of `PGroupPrime` """
        values = []
        step  = self._get_step(dur)
        for i, item in enumerate(self.data):
            delay = self._get_delay( i * step )
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

class PGroupOr(metaPGroupPrime):
    """ Used to specify `sample` values, usually from within a play string using values 
        between "bar" signs e.g. "|x2|" """
    bracket_style="|()"
    ignore = -1
    def __init__(self, seq=[]):
        metaPGroupPrime.__init__(self, seq)

        # May be changed to a Pattern
        
        if self.__class__ is not PGroupOr:
        
            return
        
        self.data = self.data[:1] # Make sure we only have 1 element for data

    def calculate_sample(self):
        sample = self.meta[0]
        if isinstance(sample, PGroupPrime):
            sample = PGroup(sample)
        elif isinstance(sample, GeneratorPattern):
            sample = sample.getitem()
        return sample

    def calculate_time(self, *args, **kwargs):
        """ Return a single value, as its always "length" 1 """
        char_delay = PGroupPrime.calculate_time(self, *args, **kwargs)[0]
        samp_delay = self.meta[0].calculate_time(*args, **kwargs) if isinstance(self.meta[0], PGroup) else 0
        return sum_delays(char_delay, samp_delay)

    def _get_delay(self, *args, **kwargs):
        return 0
    def _get_step(self, dur):
        return dur

#class PGroupFloorDiv(PGroupPrime):
#    """ Unused """
#    bracket_style="//()"

#class PGroupSub(PGroupPrime):
#    """ Unused """
#    bracket_style="-()"

class PGroupXor(metaPGroupPrime):
    """ The delay of this PGroup is specified by the last value (not included in the data) """
    bracket_style="^()"
    ignore = -1
    def __init__(self, seq=[]):
        if isinstance(seq, self.__class__):
            self.data = seq.data
            self.meta = seq.meta
            return
        metaPGroupPrime.__init__(self, seq)
        # May be changed to a Pattern
        if self.__class__ is not PGroupXor:
            return
        # Make sure we have at least 1 item of data
        if len(self.data) == 0 and len(self.meta) == 1:
            self.data = self.meta
            self.meta = [0]
    def _get_step(self, dur):
        return self.meta[0]
    def _get_delay(self, delay):
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

# Define any pattern methods that use PGroupPrimes

@PatternMethod
def offadd(self, value, dur=0.5):
    return self + PGroupXor((0, value, dur))    

@PatternMethod
def offmul(self, value, dur=0.5):
    #return self * PGroupXor(1, value).set_delay(dur)
    return self * PGroupXor((1, value, dur))

@PatternMethod
def offlayer(self, method, dur=0.5, *args, **kwargs):
    """ Zips a pattern with a modified version of itself. Method argument
        can be a function that takes this pattern as its first argument,
        or the name of a Pattern method as a string. """
    
    if callable(method):
        func = method
        args = [self] + list(args)
    else:
        func = getattr(self, method)
        assert callable(func)

    return self.zip(func(*args, **kwargs), dtype=lambda a, b: PGroupXor([a, b, dur]))
    
@PatternMethod
def amen(self, size=2):
    """ Merges and laces the first and last two items such that a
        drum pattern "x-o-" would become "(x[xo])-o([-o]-)" """
    new = []
    for n in range( LCM(len(self), 4) ):
        if  n % 4 == 0:
            new.append([self[n], PGroupPlus(self[n], modi(self, n + size))])
        elif n % 4 == size:
            new.append( [self[n]]*3+[self[n-1]] )
        elif n % 4 == size + 1:
            new.append( [PGroupPlus(self[n], self[n-1]), [self[n], self[n-1]] ] )
        else:
            new.append(self[n])
    return self.__class__(new)

@PatternMethod
def bubble(self, size=2):
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