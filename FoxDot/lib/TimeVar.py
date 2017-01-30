"""
    Time-Dependent Variable Base Class
    ==================================

    - Function of time
    - Duck typing

    - Explain inf stages: 0, 1, 2, 3

        - Stage 0: No inf value present
        - Stage 1: inf value is present but other values haven't been accessed yet
        - Stage 2: Starting values have been accessed so we are free to return a value for inf duration
        - State 3: Returning the inf value

"""

from __future__ import division

from sys import maxint as MAX_SIZE
from Patterns import Pattern, asStream, PatternContainer, GeneratorPattern
from Repeat import *
import Patterns.Operations as op
import Code

def fetch(func):
    """ Function to wrap basic lambda operators for TimeVars  """
    def eval_now(a, b):
        try:
            a = a.now()
        except:
            pass
        try:
            b = b.now()
        except:
            pass
        return func(a, b)
    return eval_now

  
class var(Repeatable):
    """ Var(values [,durs=[4]]) """

    metro = None

    def __init__(self, values, dur=4, **kwargs):

        Repeatable.__init__(self)

        self.data   = values
        self.time   = []
        self.dur    = dur
        self.bpm    = kwargs.get('bpm', None)

        self.inf_found = _inf.zero
        self.inf_value = None

        # Dynamic method for calculating values
        self.func     = op.Nil
        self.evaluate = fetch(op.Nil) 
        self.dependency = 1
        
        self.update(values, dur)

        self.current_value = None
        self.current_index = None
        self.next_value    = None

        self.current_time_block  = None

        # If the clock is not ticking, start it

        if self.metro.ticking == False:

            self.metro.start()

    @staticmethod
    def stream(values):
        return asStream(values)

    # Standard Methods
    def __str__(self):
        return str(self.now())
    def __repr__(self):
        return str(self.now())
    def __len__(self):
        return len(self.now())
    def __int__(self):
        return int(self.now())
    def __float__(self):
        return float(self.now())

    # For printing the details
    def info(self):
        return "<TimeVar(%s, %s)>" % (repr(self.values()), repr(self.durs()))
        
    # Mathematical Operators
    # ----------------------
    # Only resolve to a new TimeVar if a var, int, or float

    # + 
    def __add__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__radd__(self) for x in other))
            else:
                return other.__radd__(self)
        new = self.new(other)
        new.evaluate = fetch(op.Add)
        return new
    
    def __radd__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__add__(self) for x in other))
            else:
                return other.__add__( self)
        new = self.new(other)
        new.evaluate = fetch(op.rAdd)
        return new

    # -
    def __sub__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__rsub__(self) for x in other))
            else:
                return other.__rsub__(self)
        new = self.new(other)
        new.evaluate = fetch(op.rSub)
        return new
    def __rsub__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__sub__(self) for x in other))
            else:
                return other.__sub__(self)
        new = self.new(other)
        new.evaluate = fetch(op.Sub)
        return new

    # *
    def __mul__(self, other):
        if not isinstance(other, (var, int, float)):
            return other.__rmul__(self)
        new = self.new(other)
        new.evaluate = fetch(op.Mul)
        return new
    def __rmul__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__mul__(self) for x in other))
            else:
                return other.__mul__(self)
        new = self.new(other)
        new.evaluate = fetch(op.Mul)
        return new

    # **

    def __pow__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__row__(self) for x in other))
            else:
                return other.__rpow__(self)
        new = self.new(other)
        new.evaluate = fetch(op.rPow)
        return new

    def __rpow__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__pow__(self) for x in other))
            else:
                return other.__pow__(self)
        
        new = self.new(other)
        new.evaluate = fetch(op.Pow)
        return new
    
    # /
    def __div__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__rdiv__(self) for x in other))
            else:
                return other.__rdiv__(self)
        new = self.new(other)
        new.evaluate = fetch(op.rDiv)
        return new
    
    def __rdiv__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__div__(self) for x in other))
            else:
                return other.__div__(self)
        new = self.new(other)
        new.evaluate = fetch(op.Div)
        return new
    
    def __truediv__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__rtruediv__(self) for x in other))
            else:
                return other.__rtruediv__(self)
        new = self.new(other)
        new.evaluate = fetch(op.rDiv)
        return new
    
    def __rtruediv__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__truediv__(self) for x in other))
            else:
                return other.__truediv__(self)
        new = self.new(other)
        new.evaluate = fetch(op.Div)
        return new

    # Incremental operators (use in place of var = var + n)
    def __iadd__(self, other):
        self.data = self.data + other
        return self
    def __isub__(self, other):
        self.data = self.data - other
        return self
    def __imul__(self, other):
        self.data = self.data * other
        return self
    def __idiv__(self, other):
        self.data = self.data / other
        return self

    # Comparisons

    def __gt__(self, other):
        return float(self.now()) > float(other)

    def __lt__(self, other):
        return float(self.now()) < float(other)

    def __ge__(self, other):
        return float(self.now()) >= float(other)

    def __le__(self, other):
        return float(self.now()) >= float(other)

    # %
    def __mod__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__rmod__(self) for x in other))
            else:
                return other.__rmod__(self)
        new = self.new(other)
        new.evaulate = fetch(op.rMod)
        return new

    def __rmod__(self, other):
        if not isinstance(other, (var, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__mod__(self) for x in other))
            else:
                return other.__mod__(self)
        new = self.new(other)
        new.evaluate = fetch(op.Mod)
        return new

    #  Comparisons

    def __eq__(self, other):
        return other == self.now()

    def __ne__(self, other):
        return other != self.now()

    # Storing functions etc

    def __call__(self, *args, **kwargs):
        self.now().__call__(*args, **kwargs)
        return

    # Emulating container types 

    def __getitem__(self, other):
        new = self.new(other)
        new.dependency = self
        new.evaluate = fetch(op.rGet)
        return new

    def __iter__(self):
        for item in self.now():
            yield item

    # Update methods

    def new(self, other):
        """ Returns a new TimeVar object """
        new = var(other, self.dur, bpm=self.bpm)
        new.dependency = self
        return new

    def length(self):
        """ Returns the duration of one full cycle in beats """
        return self.time[-1][1]

    def __rshift__(self, other):
        """ var >> var([0,1,2,3],[4,8])
            var >> ([0,1,2,3],[4,8])
        """
        if type(other) == type(self):
            values = other.data
            dur    = other.dur

        elif type(other) is tuple:
            values, dur = other
            
        else:
            print "Invalid arguments"
            return self

        self.update(values, dur)
        return self

    def update(self, values, dur=None, **kwargs):
        """ Updates the TimeVar with new values """

        self.bpm = kwargs.get('bpm', self.bpm)

        # if isinstance(values, str): values = [values]

        self.data = []
        self.time = []

        #: Update the durations of each state

        if dur is not None:

            self.dur = asStream(dur)

            if any([isinstance(i, _inf) for i in self.dur]):

                self.inf_found = _inf.here

        self.data = self.stream(values)
        
        a, b = 0, 0
        
        for dur in self.dur:
            a = b
            b = a + dur
            self.time.append([a,b])

        return self

    # Evaluation methods
 
    def calculate(self, val):
        """ Returns val as modified by its dependencies """
        return self.evaluate(val, self.dependency)

    def current_time(self, beat=None):
        """ Returns the current beat value """
        if beat is None:
            beat = self.metro.now()
        if self.bpm is not None:
            beat *= (self.bpm / float(self.metro.bpm))
        return beat

    # Finding current values
    def now(self, time=None):

        time = self.current_time(time)

        loops = time // sum(self.dur)
        time  = time - (loops * sum(self.dur))

        index = int(loops * len(self.dur))

        for i in range(len(self.dur)):

            time_block = self.time[i]
            
            if time_block[0] <= time < time_block[1]:

                i = i + index
                self.current_value = self.calculate(self.data[i])

                break
            
        return self.current_value

    def copy(self):
        new = var(self.data, self.dur, bpm=self.bpm)
        return new
                   
    def durs(self):
        return self.dur

    def values(self):
        return self.data

    # 1. Methods that change the 'var' in place
    def i_invert(self):
        lrg = float(max(self.data))
        for i, item in enumerate(self.data):
            self.data[i] = (((item / lrg) * -1) + 1) * lrg
        return
        

    # Method that return an augmented NEW version of the 'var'

    def invert(self):
        new = self.new(self.data)
        lrg = float(max(new.data))
        for i, item in enumerate(new.data):
            new.data[i] = (((item / lrg) * -1) + 1) * lrg
        return new

    def lshift(self, duration):
        time = [self.dur[0]-duration] + list(self.dur[1:]) + [duration]
        return self.__class__(self.data, time)        

    def rshift(self, duration):
        time = [duration] + list(self.dur[:-1]) + [self.dur[-1]-duration]
        data = [self.data[-1]] + list(self.data)
        return self.__class__(data, time)

    def extend(self, values, dur=None):
        data = list(self.data) + list(values)
        durs = self.dur if not dur else list(self.dur) + list(asStream(dur))
        return self.__class__(data, durs)

    def shuf(self):
        pass

class Pvar(var, Pattern):
    """ Pvar([pat1, pat2], durs) """
    stream = PatternContainer
    def __init__(self, values, dur=4):
        var.__init__(self, [asStream(val) for val in values], dur)

class linvar(var):

    def __init__(self, *args, **kwargs):
        var.__init__(self, *args, **kwargs)
        self.next_value = None

    # Finding current values
    def now(self, time=None):

        time = self.current_time(time)

        loops = time // sum(self.dur)
        time  = time - (loops * sum(self.dur))

        index = int(loops * len(self.dur))

        for i in range(len(self.dur)):

            time_block = self.time[i]
            
            if time_block[0] <= time < time_block[1]:

                # We have our index

                i = i + index

                if i != self.current_index:

                    self.current_index = i
                    
                    self.current_value = self.calculate(self.data[i])
                    self.next_value    = self.calculate(self.data[i+1])
                    
                    self.current_time_block  = time_block

                break
            
        # Calculate the proportion through this time block

        p = (float(time % sum(self.dur)) - self.current_time_block[0]) / (self.current_time_block[1] - self.current_time_block[0])

        return (self.current_value * (1-p)) + (self.next_value * p)
    

class _inf(int):
    """ Used in TimeVars to stay on certain values until re-evaluated """
    zero = 0
    here = 1
    wait = 2
    done = 3
    def __new__(cls):
        return int.__new__(cls, MAX_SIZE)
    def __add__(self, other):
        return self
    def __radd__(self,other):
        return self
    def __sub__(self, other):
        return self
    def __rsub__(self, other):
        return self
    def __mul__(self, other):
        return self
    def __rmul__(self, other):
        return self
    def __div__(self, other):
        return self
    def __rdiv__(self, other):
        return 0

inf = _inf()

# TimeVar indexing of patterns

def _timevar_index(self, key):
    if isinstance(key, var):
        item = Pvar([self.data])
        item.dependency = key
        item.evaluate = fetch(op.Get)
        return item
    else:
        return self.getitem(key)

Pattern.__getitem__ = _timevar_index
