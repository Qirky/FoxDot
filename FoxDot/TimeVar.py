from Patterns import Pattern, asStream
from Patterns.Operations import modi
import Patterns.Operations as op

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

   
class TimeVar(object):

    # Used for syntax checking
    isTimeVar = True
    isplaying = False

    def __init__(self, values, dur=4, metro=None):

        self.metro  = metro
        self.data   = values
        self.time   = []
        self.dur    = dur

        # Used to stop cycling
        self.has_inf = False
        self.inf     = False
        self.inf_val = None

        # New method for calculating values
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

        if dur is not None:
            self.dur=asStream(dur)

        if InfinityObj in self.dur:
            if self.dur[-1] != InfinityObj:
                raise
            else:
                self.has_inf = True

        if isinstance(values, str):
            values = [values]

        self.data = []
        a, b = 0, -1

        for i, val in enumerate(asStream(values)):

            if isinstance(modi(self.dur,i), _infinity):

                # Replace infinity with a reasonable amount of time
                
                this_dur = GeomFill(Stretch(self.dur, i))[-1]
                
            else:

                # Get the duration for this value
                
                this_dur = modi(self.dur, i)

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

        if self.inf:
            return self.inf_value

        t = self.metro.now() % self.length()

        val = 0

        for i in range(len(self.data)):

            val = self.data[i]
            
            if self.time[i][0] <= t <= self.time[i][1]:

                break
                
                if modi(self.dur, i) == InfinityObj:
                    self.inf = True
                    self.inf_value = val

        return self.calculate(val)

    def copy(self):
        new = TimeVar(self.data, self.dur, self.metro)
        return new
                   
    def durs(self):

        return self.dur        

    def values(self):

        return self.data

def InfinityObj():
    return

class _infinity:
    """ Used in TimeVars to stay on certain values until re-evaluated """

    def __init__(self):

        pass

    def __str__(self):
        return "<TimeVar.Infinity Object>"

    def __eq__(self, other):

        return other == InfinityObj

    def __ne__(self, other):

        return other != InfinityObj

inf = Inf = _infinity()
