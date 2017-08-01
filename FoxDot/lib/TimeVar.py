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

from __future__ import absolute_import, division, print_function

from .Patterns import * # metaPattern, Pattern, asStream, PatternContainer, GeneratorPattern, PatternMethod
from .Repeat import *
from .Utils  import *
from .Patterns.Operations import *

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

 
class TimeVar(Repeatable):
    """ Var(values [,durs=[4]]) """

    metro = None

    def __init__(self, values, dur=None, **kwargs):

        Repeatable.__init__(self)

        if dur is None:

            dur = self.metro.bar_length()

        self.name   = "un-named"

        self.data   = values
        self.time   = []
        self.dur    = dur
        self.bpm    = kwargs.get('bpm', None)

        self.inf_found = _inf.zero
        self.inf_value = None

        # Dynamic method for calculating values
        self.func     = Nil
        self.evaluate = fetch(Nil) 
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

    @staticmethod
    def CreatePvarGenerator(func, *args):
        return PvarGenerator(func, *args)

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
    def __abs__(self):
        return abs(self.now())

    # For printing the details
    def info(self):
        return "<{}({}, {})>".format(self.__class__.__name__, repr(self.values()), repr(self.durs()))

    def all_values(self):
        return self.data + [self.dependency]

    def _bpm_cycle_dur(self):
        """ Returns the time, in seconds, for a var to loop to its original
            value and duration if this var is a bpm value. """
        return sum([(self.dur[i] / self.data[i]) for i in range(LCM(len(self.dur), len(self.data)) )]) * 60

    def _bpm_to_beats(self, duration, start=0):
        """ If self.data are series of bpm, how many beats occur in
            the time frame 'duration'. Used in TempoClock """

        cycle_dur = self._bpm_cycle_dur()

        start = start % self.length() # What offset to the start to apply

        n = duration // cycle_dur # How many cycles occurred in duration

        r = duration % cycle_dur  # How many seconds of the last cycle occurred

        total = n * self.length()

        i = 0

        while r > 0:

            # Work out their durations and sub from 'r' until 0

            seconds = (self.dur[i]/ self.data[i]) * 60.0

            offset  = (start / self.data[i]) * 60.0

            seconds = seconds - offset

            if seconds > 0:
                
                beats = (self.data[i] * min(seconds, r)) / 60.0
                r    -= seconds
                start = 0
                total += beats

            else:

                start -= self.dur[i]

            i += 1
        return total
        
    # Mathematical Operators
    # ----------------------
    # Only resolve to a new TimeVar if a var, int, or float

    # + 
    def __add__(self, other):
        # Run an assertion to make sure all values are valid
        #[other + item for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((self + x for x in other))
            else:
                return other.__radd__(self)
        new = self.new(other)
        new.evaluate = fetch(Add)
        return new
    
    def __radd__(self, other):
        # Run an assertion to make sure all values are valid
        #[item + other for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x + self for x in other))
            else:
                return other.__add__( self)
        new = self.new(other)
        new.evaluate = fetch(rAdd)
        return new

    # -
    def __sub__(self, other):
        # Run an assertion to make sure all values are valid
        #[item - other for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((self - x for x in other))
            else:
                return other.__rsub__(self)
        new = self.new(other)
        new.evaluate = fetch(rSub)
        return new
    def __rsub__(self, other):
        # Run an assertion to make sure all values are valid
        #[other - item for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x - self for x in other))
            else:
                return other.__sub__(self)
        new = self.new(other)
        new.evaluate = fetch(Sub)
        return new

    # *
    def __mul__(self, other):
        # Run an assertion to make sure all values are valid
        #[item * other for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((self * x for x in other))
            else:
                return other.__rmul__(self)
        new = self.new(other)
        new.evaluate = fetch(Mul)
        return new
    
    def __rmul__(self, other):
        # Run an assertion to make sure all values are valid
        #[other * item for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x * self for x in other))
            else:
                return other.__mul__(self)
        new = self.new(other)
        new.evaluate = fetch(Mul)
        return new

    # **

    def __pow__(self, other):
        # Run an assertion to make sure all values are valid
        #[item ** other for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((self ** x for x in other))
            else:
                return other.__rpow__(self)
        new = self.new(other)
        new.evaluate = fetch(rPow)
        return new

    def __rpow__(self, other):
        # Run an assertion to make sure all values are valid
        #[other ** item for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x ** self for x in other))
            else:
                return other.__pow__(self)
        
        new = self.new(other)
        new.evaluate = fetch(Pow)
        return new
    ####### todo - integer division doesn't seem to work
    # //
    def __floordiv__(self, other):
        # Run an assertion to make sure all values are valid
        #[item / other for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((self // x for x in other))
            else:
                return other.__rfloordiv__(self)
        new = self.new(other)
        new.evaluate = fetch(rFloorDiv)
        return new
    
    def __rfloordiv__(self, other):
        # Run an assertion to make sure all values are valid
        #[other / item for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x // self for x in other))
            else:
                return other.__floordiv__(self)
        new = self.new(other)
        new.evaluate = fetch(FloorDiv)
        return new

    # /
    def __truediv__(self, other):
        # Run an assertion to make sure all values are valid
        #[item / other for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((self / x for x in other))
            else:
                return other.__rtruediv__(self)
        new = self.new(other)
        new.evaluate = fetch(rDiv)
        return new
    
    def __rtruediv__(self, other):
        # Run an assertion to make sure all values are valid
        #[other / item for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x / self for x in other))
            else:
                return other.__truediv__(self)
        new = self.new(other)
        new.evaluate = fetch(Div)
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
        # Run an assertion to make sure all values are valid
        #[other.__rmod__(item) for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__rmod__(self) for x in other))
            else:
                return other.__rmod__(self)
        new = self.new(other)
        new.evaluate = fetch(rMod)
        return new

    def __rmod__(self, other):
        # Run an assertion to make sure all values are valid
        #[other.__mod__(item) for item in self.all_values()]
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) in (tuple, list):
                return other.__class__((x.__mod__(self) for x in other))
            else:
                return other.__mod__(self)
        new = self.new(other)
        new.evaluate = fetch(Mod)
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
        new.evaluate = fetch(rGet)
        return new

    def __iter__(self):
        for item in self.now():
            yield item

    # Update methods

    def new(self, other):
        """ Returns a new TimeVar object """
        new = self.__class__(other, self.dur, bpm=self.bpm)
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
            print("Invalid arguments")
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

class Pvar(TimeVar, Pattern):
    """ A TimeVar that represents Patterns that change over time e.g.
        ```
        >>> a = Pvar([ [0,1,2,3], [4,5] ], 4)
        >>> print a # time is 0
        P[0, 1, 2, 3]
        >>> print a # time is 4
        P[4, 5]
    """
    stream = PatternContainer
    def __init__(self, values, dur=None, **kwargs):

        try:

            data = [asStream(val) for val in values]

        except:

            data = [values]
        
        TimeVar.__init__(self, data, dur, **kwargs)

    def __add__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(Add)
        return new

    def __radd__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rAdd)
        return new
    
    def __sub__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(Sub)
        return new
    
    def __rsub__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rSub)
        return new

    def __mul__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(Mul)
        return new
    
    def __rmul__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rMul)
        return new
    
    def __div__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(Div)
        return new
    
    def __rdiv__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rDiv)
        return new
    
    def __truediv__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(Div)
        return new
    
    def __rtruediv__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rDiv)
        return new
    
    def __floordiv__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(FloorDiv)
        return new
    
    def __rfloordiv__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rFloorDiv)
        return new

    def __pow__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(Pow)
        return new

    def __rpow__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rPow)
        return new

    def __mod__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(Mod)
        return new

    def __rmod__(self, other):
        new = self.new(asStream(other))
        new.evaluate = fetch(rMod)
        return new

    def __or__(self, other):
        # Used when piping patterns together
        new = self.new(PatternContainer(other))
        new.evaluate = fetch(rOr)
        return new

    def __ror__(self, other):
        # Used when piping patterns together
        new = self.new(PatternContainer(other))
        new.evaluate = fetch(Or)
        return new


class PvarGenerator(Pvar):
    """ If a TimeVar is used in a Pattern function e.g. `PDur(var([3,5]), 8)`
        then a `PvarGenerator` is returned. Each argument is stored as a TimeVar
        and the function is called whenever the arguments are changed
    """
    def __init__(self, func, *args):
        self.func = func
        self.args = [(arg if isinstance(arg, TimeVar) else TimeVar(arg)) for arg in args]
        self.last_args = []
        self.last_data = []
        self.evaluate = fetch(Nil) 
        self.dependency = 1
        
    def now(self):
        new_args = [arg.now() for arg in self.args]
        if new_args != self.last_args:
            self.last_args = new_args
            self.last_data = self.func(*self.last_args)
        return self.calculate(self.last_data)

    def new(self, other):
        new = self.__class__(lambda x: x, other)
        new.dependency = self
        return new
    

class _continuous_var(TimeVar):

    def __init__(self, *args, **kwargs):
        TimeVar.__init__(self, *args, **kwargs)
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

        return self.get_timevar_value(p)


class linvar(_continuous_var):
    def get_timevar_value(self, prop):
        return (self.current_value * (1-prop)) + (self.next_value * prop)

class expvar(_continuous_var):
    def get_timevar_value(self, prop):
        prop *= prop
        return (self.current_value * (1-prop)) + (self.next_value * prop)
    

class _inf(int):
    """ Used in TimeVars to stay on certain values until re-evaluated """
    zero = 0
    here = 1
    wait = 2
    done = 3
    def __new__(cls):
        return int.__new__(cls, 0)
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

# Store and updates TimeVars

class _var_dict(object):
    """
        This is the TimeVar generator used in FoxDot. Calling it like `var()`
        returns a TimeVar but setting an attribute `var.foo = var([1,2],4)` will
        update the TimeVar that is already in `var.foo`.

        In short, using `var.name = var([i, j])` means you don't have to delete
        some of the text and replace it with `var.name.update([k, l])` you can
        just use `var.name = var([k, l])` and the contents of the var will be
        updated everywhere else in the program.
    """
    
    def __init__(self):
        self.__vars = {}
    @staticmethod
    def __call__(*args, **kwargs):
        return TimeVar(*args, **kwargs)
    def __setattr__(self, name, value):
        if name != "__vars" and isinstance(value, TimeVar):
            if name in self.__vars:
                if value.__class__ != self.__vars[name].__class__:
                    self.__vars[name].__class__ = value.__class__
                self.__vars[name].__dict__ = value.__dict__
            else:
                self.__vars[name] = value
            return
        object.__setattr__(self, name, value)
    def __getattr__(self, name):
        if name in self.__vars:
            value = self.__vars[name]
        else:
            value = object.__getattr__(self, name)
        return value

var = _var_dict()

# Give Main.Pattern a reference to TimeVar class
Pattern.TimeVar = TimeVar

@PatternMethod
def __getitem__(self, key):
    if isinstance(key, TimeVar):
        # Create a TimeVar of a PGroup that can then be indexed by the key
        item = TimeVar(tuple(self.data))
        item.dependency = key
        item.evaluate = fetch(Get)
        return item
    else:
        return self.getitem(key)
