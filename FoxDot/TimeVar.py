from sys import maxint as MAX_SIZE
from Patterns import Pattern, asStream
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

# Misc. Functions

def Ramp(start=0, end=1, dur=8, step=0.25):
    size = dur/float(step)
    return var([start + end * n/size for n in range(int(size))], step)

def iRamp(start=0, end=1, dur=8, step=0.25):
    size = dur/float(step)
    return var([start + end * n/size for n in range(int(size))] + [end], [step]*int(size)+[inf])


   
class TimeVar(Code.LiveObject):

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

    def __init__(self, values, dur=4, metro=None):

        self.metro  = metro
        self.data   = values
        self.time   = []
        self.dur    = dur

        self.inf_found = _inf.zero
        self.inf_value = None

        # Dynamic method for calculating values

        self.evaluate = fetch(op.Nil)
        self.dependency = 1
        
        self.update(values, dur)

    # Standard Methods
    def __str__(self):
        return  str(self.now())
    def __repr__(self):
        return "<TimeVar(%s, %s)>" % (repr(self.values()), repr(self.durs()))
    def __len__(self):
        return len(self.now())
    def __int__(self):
        return int(self.now())
    def __float__(self):
        return float(self.now())
        
    # Mathematical Operators

    # + 
    def __add__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Add)
        return new
    def __radd__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Add)
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
    def __truediv__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.rDiv)
        return new
    def __rtruediv__(self, other):
        new = self.new(other)
        new.evaluate = fetch(op.Div)
        return new

    #  Comparisons

    def __eq__(self, other):
        return other == self.now()

    def __ne__(self, other):
        return other != self.now()

    # Emulating container types 

    def __getitem__(self, key):
        return self.now()[key]

    def __iter__(self):
        for item in self.now():
            yield item

    # Update methods

    def new(self, other):
        """ Returns a new TimeVar object """
        if isinstance(other, self.__class__):
            new = other
        else:     
            new = TimeVar(other, self.dur, self.metro)

        new.dependency = self
        
        return new

    def length(self):
        """ Returns the duration of one full cycle in beats """
        return self.time[-1][1] + 1

    def update(self, values, dur=None):
        """ Updates the TimeVar with new values """

        #: If updated with a TimeVar object, copy the attribute dict
        
        if isinstance(values, self.__class__):
            self.__dict__ = values.__dict__
            return self
        
        # if isinstance(values, str): values = [values]

        self.data = []
        self.time = []
        a, b = 0, -1

        #: Update the durations of each state
        
        self.dur = self.dur if dur is None else asStream(dur)

        if dur is not None:

            if any([isinstance(i, _inf) for i in dur]):

                self.inf_found = _inf.here

            self.dur = dur

        for i, val in enumerate(asStream(values)):
              
            this_dur = op.modi(self.dur, i)

            a = b + 1
            b = a + (self.metro.steps * this_dur) - 1
    
            self.data.append( val )
            self.time.append((a,b))

            # The contained data should be a Pattern

            self.data = asStream( self.data )

        return self

    # Evaluation methods
 
    def calculate(self, val):
        """ Returns val as modified by its dependencies """
        return self.evaluate(val, self.dependency)


    def now(self):
        """ Returns the value from self.data for time t in self.metro """

        if self.inf_found == 3:

            val = self.inf_value

        else:

            t = self.metro.now() % self.length()

            val = 0

            for i in range(len(self.data)):                

                val = self.data[i]
                
                if self.time[i][0] <= t <= self.time[i][1]:

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


class _inf(int):
    """ Used in TimeVars to stay on certain values until re-evaluated """
    zero = 0
    here = 1
    wait = 2
    done = 3
    def __new__(cls):
        return int.__new__(cls, MAX_SIZE)

inf = _inf()
