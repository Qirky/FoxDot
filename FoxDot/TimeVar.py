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

from sys import maxint as MAX_SIZE
from math import modf
from Patterns import Pattern, asStream, PatternContainer
import Patterns.Sequences as pat
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

  
class Var(Code.LiveObject):
    """ Var(values [,durs=[4]]) """

    metro = None

    def __init__(self, values, dur=4, **kwargs):

        self.data   = values
        self.time   = []
        self.dur    = dur
        self.bpm    = kwargs.get('bpm', None)

        self.inf_found = _inf.zero
        self.inf_value = None

        # Dynamic method for calculating values

        self.evaluate = fetch(op.Nil)
        self.dependency = 1
        
        self.update(values, dur)

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

    # + 
    def __add__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Add)
        return new
    def __radd__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.rAdd)
        return new 

    # -
    def __sub__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.rSub)
        return new
    def __rsub__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Sub)
        return new

    # *
    def __mul__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Mul)
        return new
    def __rmul__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Mul)
        return new
    
    # /
    def __div__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.rDiv)
        return new
    def __rdiv__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Div)
        return new
    def __truediv__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.rDiv)
        return new
    def __rtruediv__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Div)
        return new

    # %
    def __mod__(self, other):
        return float(self.now()) % other

    def __rmod__(self, other):
        return other % float(self.now())
    
####        new = self.new(other)
####        new.evaulate = fetch(op.rMod)
####        return new
##
##    def __rmod__(self, other): #works
##        new = self.new(other)
##        new.evaluate = fetch(op.Mod)
##        return new

    #  Comparisons

    def __eq__(self, other):
        return other == self.now()

    def __ne__(self, other):
        return other != self.now()

    # Emulating container types 

    def __getitem__(self, other):
        new = self.new(other)
        new.dependency = self
        new.evaluate = fetch(op.rGet)
        return new

    def __index__(self):
        return int(self)

    def __iter__(self):
        for item in self.now():
            yield item

    # Update methods

    def new(self, other):
        """ Returns a new TimeVar object """
            
        if isinstance(other, Var):
            new = other
        else:     
            new = Var(other, self.dur, bpm=self.bpm)

        new.dependency = self
        
        return new

    def length(self):
        """ Returns the duration of one full cycle in beats """
        return self.time[-1][1]

    def update(self, values, dur=None, **kwargs):
        """ Updates the TimeVar with new values """

        self.bpm = kwargs.get('bpm', self.bpm)

        #: If updated with a TimeVar object, copy the attribute dict
        
        if isinstance(values, self.__class__):
            self.__dict__ = values.__dict__
            return self
        
        # if isinstance(values, str): values = [values]

        self.data = []
        self.time = []
        a, b = 0, 0

        #: Update the durations of each state

        if dur is not None:

            self.dur = asStream(dur)

            if any([isinstance(i, _inf) for i in self.dur]):

                self.inf_found = _inf.here

        # Make equal size

        values = self.stream(values)

        length = max(len(values), len(self.dur))

        values.stretch(length)
        self.dur.stretch(length)

        # Loop over the values and define time frame

        for i, val in enumerate(values):
              
            this_dur = op.modi(self.dur, i)

            a = b
            b = a + this_dur
    
            self.data.append( val )
            self.time.append((a,b))

        # The contained data should be a Pattern

        self.data = self.stream( self.data )

        return self

    # Evaluation methods
 
    def calculate(self, val):
        """ Returns val as modified by its dependencies """
        return self.evaluate(val, self.dependency)

    def current_time(self):
        """ Returns the current beat value """
        beat = self.metro.now()
        if self.bpm is not None:
            beat *= (self.bpm / float(self.metro.bpm))
        t = beat % self.length()
        return t

    def now(self):
        """ Returns the value from self.data for time t in self.metro """

        if self.inf_found == 3:

            val = self.inf_value

        else:

            # If using a different bpm to the clock

            t = self.current_time()

            val = 0

            for i in range(len(self.data)):                

                val = self.data[i]
                
                if self.time[i][0] <= t < self.time[i][1]:

                    if isinstance(op.modi(self.dur, i), _inf):

                        if self.inf_found == _inf.wait:

                            self.inf_found = _inf.done

                            self.inf_value = val

                    elif self.inf_found == _inf.here:

                        self.inf_found = _inf.wait

                    break
                
        return self.calculate(val)

    def copy(self):
        new = TimeVar(self.data, self.dur, self.metro)
        return new
                   
    def durs(self):
        return self.dur        

    def values(self):
        return self.data

    # Methods that do cool stuff

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

var = Var

class PVar(Var, Pattern):
    """ Pvar([pat1, pat2], durs) """
    stream = PatternContainer
    def __init__(self, values, dur=4):
        Var.__init__(self, [asStream(val) for val in values], dur)

Pvar = PVar

class linvar(Var):
    
    def now(self):

        t = self.current_time()

        for i in range(len(self.data)):

            val = self.data[i]
            
            if self.time[i][0] <= t < self.time[i][1]:

                break

        # Proportion of the way between values
        
        p = (float(t) - self.time[i][0]) / (self.time[i][1] - self.time[i][0])

        # Next value

        q = op.modi(self.data, i + 1)

        # Calculate and add dependencies

        val = (val * (1-p)) + (q * p)

        return self.calculate(val)
    


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

class const:
    """ A number value that cannot be changed """
    def __init__(self, value):
        self.value=value
    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)
    def __add__(self, other):
        return self.value
    def __radd__(self, other):
        return self.value
    def __sub__(self, other):
        return self.value
    def __rsub__(self, other):
        return self.value
    def __mul__(self, other):
        return self.value
    def __rmul__(self, other):
        return self.value
    def __div__(self, other):
        return self.value
    def __rdiv__(self, other):
        return self.value
