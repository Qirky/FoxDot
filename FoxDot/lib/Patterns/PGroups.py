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

class PGroupFloorDiv(PGroupPrime):
    """ Unused """
    bracket_style="//()"

class PGroupMod(PGroupPrime):
    """ Unused """
    bracket_style="%()"

class PGroupSub(PGroupPrime):
    """ Unused """
    bracket_style="-()"

class PGroupXor(PGroupPrime):
    """ Unused """
    bracket_style="^()"

class PGroupAnd(PGroupPrime):
    """ Unused """
    bracket_style="&()"
    delay = 0
    def __init__(self, args):
        PGroupPrime.__init__(self, args[0])
        if len(args) > 0:
            self.delay = args[1]
    def calculate_step(self, i, dur):
        return i * self.delay

class PGroupOr(PGroupPrime):
    """ Unused """
    bracket_style="|()"

# Define any pattern methods that use PGroupPrimes
    
@PatternMethod
def amen(self, size=2):
    """ Merges and laces the first and last two items such that a
        drum pattern "x-o-" would become "(x[xo])-o([-o]-)" """
    new = []

    for n in range(len(self.data)):

        if  n % 4 == 0:

            new.append([self.data[n], PGroupStar(self.data[n], modi(self.data, n + size))])

        elif n % 4 == 2:

            new.append( [self.data[n]]*3+[self.data[n-1]] )

        elif n % 4 == 3:

            new.append( [PGroupStar(self.data[n], self.data[n-1]), [self.data[n], self.data[n-1]] ] )

        else:

            new.append(self.data[n])
    
    return self.__class__(new)
