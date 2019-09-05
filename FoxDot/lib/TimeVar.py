"""
Time-Dependent Variables (TimeVar)

TODO: using __call__ -> go through getattribute and check instead of already having a __call__

"""

from __future__ import absolute_import, division, print_function

from .Patterns import *
from .Utils  import *
from .Patterns.Operations import *
from .Constants import inf 

from time import time

def fetch(func):
    """ Function to wrap basic lambda operators for TimeVars  """
    def eval_now(a, b):
        if isinstance(a, TimeVar):
            a = a.now()
        if isinstance(b, TimeVar):
            b = b.now()
        return func(a, b)
    return eval_now


class TimeVar(object):
    """ Var(values [,durs=[4]]) """

    metro = None
    depth = 128

    def __init__(self, values, dur=None, start=0, **kwargs):

        if dur is None:

            dur = self.metro.bar_length()

        self.name     = "un-named"

        self.start_time = float(start) # offset

        self.values   = values
        self.dur      = dur
        self.bpm      = kwargs.get('bpm', None)

        self.get_seconds = bool(kwargs.get('seconds', False))

        # Dynamic method for calculating values
        self.func     = Nil
        self.evaluate = fetch(Nil)
        self.dependency = None

        self.update(values, dur)

        self.current_value = None
        self.current_index = 0
        self.next_value    = None
        self.next_time     = 0
        self.prev_time     = 0
        self.next_index    = 0

        # Private flags

        self.__accessed = False
        self.__inf_index = None

        self.proportion    = 0

        # If the clock is not ticking, start it

        if self.metro.ticking == False:

            self.metro.start()

    def json_value(self):
        """ Returns data about this TimeVar that can be sent over a network as JSON  """
        ## pickle?
        return [str(self.__class__.__name__), list(self.values), list(self.dur)]

    @classmethod
    def set_clock(cls, tempo_clock):
        cls.metro = tempo_clock
        return

    @classmethod
    def help(cls):
        return print(cls.__doc__)

    @staticmethod
    def stream(values):
        return asStream(values)

    @staticmethod
    def CreatePvarGenerator(func, *args, **kwargs):
        return PvarGenerator(func, *args, **kwargs)

    # Standard dunder methods
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
        return "<{}({}, {})>".format(self.__class__.__name__, repr(self.get_values()), repr(self.get_durs()))

    def all_values(self):
        """ Displays the values and the dependency value - useful for debugging """
        return self.value + [self.dependency]

    # Update methods

    def new(self, other):
        """ Returns a new TimeVar object """
        # new = TimeVar(other, self.dur, bpm=self.bpm)
        new = ChildTimeVar(other)
        new.dependency = self
        return new

    def update(self, values, dur=None, **kwargs):
        """ Updates the TimeVar with new values.
        """

        self.bpm = kwargs.get('bpm', self.bpm)

        #: Update the durations of each state

        if dur is not None:

            self.dur = asStream(dur)

        self.values = self.stream(values)

        return self

    def get_current_index(self, time=None):
        """ Returns the index of the value currently represented """

        # Get the time value if not from the Clock

        time = self.get_current_time(time) - self.start_time

        if self.get_inf_index() is not None:

            return self.get_inf_index()

        if time >= self.next_time:

            while True:

                next_dur = self.dur[self.next_index]

                self.next_time, self.prev_time = self.next_time + next_dur, self.next_time

                # If we find an "inf"

                if self.check_for_inf(next_dur):

                    self.set_inf_index(self.next_index)

                    return self.get_inf_index()

                self.next_index += 1

                if self.next_time >= time:

                    break

        # Store the % way through this value's time

        try:

            self.proportion = float((time - self.prev_time) / (self.next_time - self.prev_time))

        except ZeroDivisionError:

            self.proportion = 1.0

        # The current index is the next index minus one

        self.current_index = self.next_index - 1

        # Flag we have accessed the value

        self.flag_accessed()

        return self.current_index

    # Inf

    def set_inf_index(self, value):
        self.__inf_index = int(value)
        return

    def get_inf_index(self):
        self.proportion = 0
        return self.__inf_index

    def check_for_inf(self, duration):
        return (self.__accessed and duration == inf)

    def flag_accessed(self):
        self.__accessed = True
        return

    # Evaluation methods

    def calculate(self, val): # maybe rename to resolve
        """ Returns val as modified by its dependencies """
        return self.evaluate(val, self.dependency)

    def get_current_time(self, beat=None):
        """ Returns the current beat value """
        # Return elapsed time in seconds if get_seconds flag is True
        if self.get_seconds is True:
            return float(self.metro.time)
        # Else return the beat
        if beat is None:
            beat = self.metro.now()
        if self.bpm is not None:
            beat *= (self.bpm / float(self.metro.bpm))
        return float(beat)

    def now(self, time=None):
        """ Returns the value currently represented by this TimeVar """

        i = self.get_current_index(time)
        self.current_value = self.calculate(self.values[i])
        
        return self.current_value

    def copy(self):
        new = var(self.values, self.dur, bpm=self.bpm)
        return new

    def get_durs(self):
        return self.dur

    def get_values(self):
        return self.values

    # 1. Methods that change the 'var' in place
    def i_invert(self):
        lrg = float(max(self.values))
        for i, item in enumerate(self.values):
            self.values[i] = (((item / lrg) * -1) + 1) * lrg
        return

    # Method that return an augmented NEW version of the 'var'

    def invert(self):
        new = self.new(self.values)
        lrg = float(max(new.data))
        for i, item in enumerate(new.data):
            new.data[i] = (((item / lrg) * -1) + 1) * lrg
        return new

    def lshift(self, duration):
        time = [self.dur[0]-duration] + list(self.dur[1:]) + [duration]
        return self.__class__(self.values, time)

    def rshift(self, duration):
        time = [duration] + list(self.dur[:-1]) + [self.dur[-1]-duration]
        data = [self.values[-1]] + list(self.values)
        return self.__class__(data, time)

    def extend(self, values, dur=None):
        data = list(self.values) + list(values)
        durs = self.dur if not dur else list(self.dur) + list(asStream(dur))
        return self.__class__(data, durs)

    def shuf(self):
        pass

    # Mathmetical operators

    def math_op(self, other, op):
        """ Performs the mathematical operation between self and other. "op" should 
            be the string name of a dunder method  e.g. __mul__ """
        if not isinstance(other, (TimeVar, int, float)):
            if type(other) is tuple:
                return PGroup([getattr(self, op).__call__(x) for x in other])
            elif type(other) is list:
                return Pattern([getattr(self, op).__call__(x) for x in other])
            else:
                return getattr(other, get_inverse_op(op)).__call__(self)
        return other

    def set_eval(self, func):
        self.evaluate = fetch(func)
        self.func     = func
        return

    def __add__(self, other):
        new = self.math_op(other, "__add__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(Add)
        return new

    def __radd__(self, other):
        new = self.math_op(other, "__radd__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(rAdd)
        return new

    def __sub__(self, other):
        new = self.math_op(other, "__sub__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(rSub)
        return new

    def __rsub__(self, other):
        new = self.math_op(other, "__rsub__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(Sub)
        return new

    def __mul__(self, other):
        new = self.math_op(other, "__mul__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(Mul)
        return new

    def __rmul__(self, other):
        new = self.math_op(other, "__rmul__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(Mul)
        return new

    def __pow__(self, other):
        new = self.math_op(other, "__pow__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(rPow)
        return new

    def __rpow__(self, other):
        new = self.math_op(other, "__rpow__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(Pow)
        return new

    def __floordiv__(self, other):
        new = self.math_op(other, "__floordiv__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(rFloorDiv)
        return new

    def __rfloordiv__(self, other):
        new = self.math_op(other, "__rfloordiv__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(FloorDiv)
        return new

    def __truediv__(self, other):
        new = self.math_op(other, "__truediv__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(rDiv)
        return new

    def __rtruediv__(self, other):
        new = self.math_op(other, "__rtruediv__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(Div)
        return new

    # Incremental operators (use in place of var = var + n)
    def __iadd__(self, other):
        self.values = self.values + other
        return self
    def __isub__(self, other):
        self.values = self.values - other
        return self
    def __imul__(self, other):
        self.values = self.values * other
        return self
    def __idiv__(self, other):
        self.values = self.values / other
        return self

    # Comparisons -- todo: return TimeVars

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
        new = self.math_op(other, "__mod__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(rMod)
        return new

    def __rmod__(self, other):
        new = self.math_op(other, "__rmod__")
        if not isinstance(other, (TimeVar, int, float)):
            return new
        new = self.new(other)
        new.evaluate = fetch(Mod)
        return new

    #  Comparisons -- todo: return TimeVar

    def __eq__(self, other):
        return other == self.now()

    def __ne__(self, other):
        return other != self.now()

    # Storing functions etc

    # def __call__(self, *args, **kwargs):
    #     """ A TimeVar can store functions and will call the current item with this method """
    #     if callable(self.now()):
    #         return self.now().__call__(*args, **kwargs)
    #     else:
    #         return self.now()

    # Emulating container types

    def __getitem__(self, other):
        new = self.new(other)
        new.dependency = self
        new.evaluate = fetch(rGet)
        return new

    def __iter__(self):
        for item in self.now():
            yield item

    def transform(self, func):
        """ Returns a new TimeVar based on a func """
        new = self.new(0)
        new.dependency = self
        new.evaluate = fetch(lambda a, b: func(b))
        return new

class ChildTimeVar(TimeVar):
    """ When a new TimeVar is created using a function such as addition,
        e.g. var([0,2]) + 2, then a ChildTimeVar is created that contains a
        single value but also creates a new ChildTimeVar when operated upon
        and behaves just as a TimeVar does."""
    def now(self, time=None):
        self.current_value = self.calculate(self.values[0])
        return self.current_value

class linvar(TimeVar):
    def now(self, time=None):
        """ Returns the value currently represented by this TimeVar """
        i = self.get_current_index(time)
        self.current_value = self.calculate(self.values[i])
        self.next_value    = self.calculate(self.values[i + 1])
        return self.get_timevar_value()

    def get_timevar_value(self):
        return (self.current_value * (1-self.proportion)) + (self.next_value * self.proportion)

class expvar(linvar):
    def get_timevar_value(self):
        self.proportion *= self.proportion
        return (self.current_value * (1-self.proportion)) + (self.next_value * self.proportion)

import math

class sinvar(linvar):
    def get_timevar_value(self):
        d = self.current_value  > self.next_value
        x = (self.proportion * 90) + (d * 270)
        self.proportion = math.sin(math.radians(x)) + int(d)
        return (self.current_value * (1-self.proportion)) + (self.next_value * self.proportion)

PATTERN_METHODS = Pattern.get_methods()

class Pvar(TimeVar):
    """ A TimeVar that represents Patterns that change over time e.g.
        ::

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


    def __get_pattern_attr(self, attr):
        """ Returns a function that transforms the patterns of this Pvar if the attr
            is a Pattern method, if not it returns the attribute  for the current pattern
        """

        pattern_attr = getattr(self.now(), attr)

        if callable(pattern_attr):

            def get_new_pvar(*args, **kwargs):

                # If this is the root Pvar, change the values

                if self.dependency is None:

                    print(len(self.values))

                    new_values = [getattr(pat, attr)(*args, **kwargs) for pat in self.values]

                    return Pvar(new_values, dur=self.dur)

                else:

                    # Get the "parent" Pvar and re-apply the connecting function

                    new_pvar = getattr(self.dependency, attr)(*args, **kwargs)

                    new_item = self.func(new_pvar, self.original_value)

                    return new_item

            return get_new_pvar

        else:

            return pattern_attr

    def getitem(self, index, *args, **kwargs):
        """ Returns a TimeVar based on getting the index of this Pattern """
        return TimeVar(0).transform(lambda e: self.now().getitem(index))

    def __getattr__(self, attr):
        """ (Python 2 compatability) Override for accessing pattern methods. Returns a new
            Pvar that has been "transformed" using the method such that then method also
            applies when values have been updated.  """

        try:

            return object.__getattr__(self, attr)

        except AttributeError:

            return self.__get_pattern_attr(attr)

    def __getattribute__(self, attr):
        """ Override for accessing pattern methods. Returns a new
            Pvar that has been "transformed" using the method such that then method also
            applies when values have been updated.  """

        try:

            return object.__getattribute__(self, attr)

        except AttributeError:

            return self.__get_pattern_attr(attr)

    def new(self, other):
        # new = Pvar([other], dur=self.dur)
        new = ChildPvar(other)
        new.original_value = other
        new.dependency = self
        return new

    def __getitem__(self, other):
        """ Return a single timevar when using getitem """
        new = ChildTimeVar(other)
        new.dependency = self
        new.evaluate = fetch(rGet)
        return new

    def set_eval(self, func):
        self.evaluate = fetch(func)
        self.func     = func
        return

    def __add__(self, other):
        new = self.new(other)
        new.set_eval(rAdd)
        return new

    def __radd__(self, other):
        new = self.new((other))
        new.set_eval(Add)
        return new

    def __sub__(self, other):
        new = self.new((other))
        new.set_eval(rSub)
        return new

    def __rsub__(self, other):
        new = self.new((other))
        new.set_eval(Sub)
        return new

    def __mul__(self, other):
        new = self.new((other))
        new.set_eval(rMul)
        return new

    def __rmul__(self, other):
        new = self.new((other))
        new.set_eval(Mul)
        return new

    def __div__(self, other):
        new = self.new((other))
        new.set_eval(rDiv)
        return new

    def __rdiv__(self, other):
        new = self.new((other))
        new.set_eval(Div)
        return new

    def __truediv__(self, other):
        new = self.new((other))
        new.set_eval(rDiv)
        return new

    def __rtruediv__(self, other):
        new = self.new((other))
        new.set_eval(Div)
        return new

    def __floordiv__(self, other):
        new = self.new((other))
        new.set_eval(rFloorDiv)
        return new

    def __rfloordiv__(self, other):
        new = self.new((other))
        new.set_eval(FloorDiv)
        return new

    def __pow__(self, other):
        new = self.new((other))
        new.set_eval(rPow)
        return new

    def __rpow__(self, other):
        new = self.new((other))
        new.set_eval(Pow)
        return new

    def __mod__(self, other):
        new = self.new((other))
        new.set_eval(rMod)
        return new

    def __rmod__(self, other):
        new = self.new((other))
        new.set_eval(Mod)
        return new

    def __or__(self, other):
        # Used when piping patterns together
        new = self.new(PatternContainer(other))
        new.set_eval(rOr)
        return new

    def __ror__(self, other):
        # Used when piping patterns together
        new = self.new(PatternContainer(other))
        new.set_eval(Or)
        return new

    def transform(self, func):
        """ Returns a Pvar based on a transformation function, as opposed to
            a mathematical operation"""
        new = self.new(self)
        new.set_eval(lambda a, b: b.transform(func))
        return new

class ChildPvar(Pvar):
    def now(self, time=None):
        self.current_value = self.calculate(self.values[0])
        return self.current_value


class PvarGenerator(Pvar):
    """ If a TimeVar is used in a Pattern function e.g. `PDur(var([3,5]), 8)`
        then a `PvarGenerator` is returned. Each argument is stored as a TimeVar
        and the function is called whenever the arguments are changed
    """
    def __init__(self, func, *args, **kwargs):
        self.p_func = func # p_func is the Pattern function e.g. PDur but self.func is created when operating on this PvarGenerator
        
        self.args = []

        if "pattern" in kwargs:

            self.args.append(kwargs["pattern"])
        
        self.args.extend( [(arg if isinstance(arg, TimeVar) else TimeVar(arg)) for arg in args] )

        self.last_args = []
        self.last_data = []
        self.evaluate = fetch(Nil)
        self.dependency = None

    def info(self):
        return "<{} {}>".format(self.__class__.__name__, self.func.__name__ + str(tuple(self.args)))

    def now(self):
        new_args = [arg.now() if isinstance(arg, TimeVar) else arg for arg in self.args]
        if new_args != self.last_args:
            self.last_args = new_args
            self.last_data = self.p_func(*self.last_args)
        pat = self.calculate(self.last_data)
        return pat

    def new(self, other):
        # new = Pvar([other]) # TODO -- test this
        new = self.__class__(lambda x: x, other)
        new.original_value = other
        new.dependency = self
        return new

    def set_eval(self, func):
        self.evaluate = fetch(func)
        self.func     = func
        return

    def __getattribute__(self, attr):
        # If it's a method, only return the method if its new, transform, or a dunder
        if attr in Pattern.get_methods():   
            
            if attr not in ("new", "now", "transform") and not attr.startswith("__"):

                # return a function that transforms the patterns of the  root Pvar

                def get_new_pvar_gen(*args, **kwargs):

                    # If this is the root Pvar, change the values

                    if self.dependency is None:

                        # Create a new function that combines the original *plus* the method

                        def new_func(*old_args, **old_kwargs):

                            return getattr(self.p_func(*old_args, **old_kwargs), attr)(*args, **kwargs)

                        return PvarGenerator(new_func, *self.args)

                    else:

                        # Get the "parent" Pvar and re-apply the connecting function

                        new_pvar_gen = getattr(self.dependency, attr)(*args, **kwargs)

                        return self.func(new_pvar_gen, self.original_value)

                return get_new_pvar_gen
                
        return object.__getattribute__(self, attr)

class PvarGeneratorEx(PvarGenerator):
    """ Un-Documented """
    def __init__(self, func, *args):
        self.func = func
        self.args = list(args)
        self.last_args = []
        self.last_data = []
        self.evaluate = fetch(Nil)
        self.dependency = 1

class mapvar(Pvar):
    """ Like a `Pvar`, the `mapvar` returns a whole `Pattern` as opposed to a single
        value, but instead of using the global clock to find the current value it
        uses the value in an instance of the `PlayerKey` class or another `TimeVar`. """
    def __init__(self, key, mapping, default=0):
        TimeVar.__init__(self, [])
        self.key     = key
        self.values  = {key: asStream(value) for key, value in mapping.items()}
        self.default = asStream(default)

    def get_current_index(self, time=None):
        self.current_index = self.key.now()
        return self.current_index

    def now(self, time=None):
        """ Returns the value currently represented by this TimeVar """
        i = self.get_current_index(time)
        self.current_value = self.calculate(self.values.get(i, self.default))
        return self.current_value

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
            try:
                value = object.__getattr__(self, name)
            except AttributeError:
                err = NameError("'var.{}' does not exist.".format(name))
                raise err
        return value

var = _var_dict()

# Give Main.Pattern a reference to TimeVar classes
Pattern.TimeVar       = TimeVar
Pattern.PvarGenerator = PvarGenerator
Pattern.Pvar          = Pvar
