from __future__ import absolute_import, division, print_function

from .Patterns import *
from .TimeVar import TimeVar
from .Utils import recursive_any
from functools import partial


class NumberKey(object):
    """ An object that acts like a number but may have dependencies when returing its
        value. These are used when returing Player object attribute values accessed via
        `getattr` e.g. `p1.dur` or `getattr(p1, "dur")`. The parent attribute is the Player
        that contains the key or the referenced key in the case that the value has been
        maniupulated. e.g. if `p1` is using `p2.degree` then `p1.degree.parent == p1` and 
        `p1.degree.value.parent == p2`.
    """

    def __init__(self, value, reference):
        # the number to store/update
        self.value = value
        # reference to another number key that this is linked to
        self.other = reference
        # This is the Player object whose attribute this is fetching / chained to
        self.parent = self.other.parent if isinstance(self.other, NumberKey) else None

    # Storing mathematical operations

    @staticmethod
    def calculate(x, y):
        return x

    @staticmethod
    def convert_to_pattern(value):
        if isinstance(value,  list):
            value = Pattern(value)
        elif isinstance(value, tuple):
            value = PGroup(value)
        elif not isinstance(value, metaPattern):
            value = Pattern(value)
        return value
    
    def __add__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (Pattern, GeneratorPattern)):
            return other.__radd__(self)
        new = self.child(other)
        new.calculate = Add
        return new

    def __radd__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, metaPattern):
            return other.__add__(self)
        new = self.child(other)
        new.calculate = Add
        return new
    
    def __sub__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__rsub__(self)
        new = self.child(other)
        new.calculate = rSub
        return new
    
    def __rsub__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__sub__(self)
        new = self.child(other)
        new.calculate = Sub
        return new
    
    def __mul__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (Pattern, GeneratorPattern)): # was metaPattern before
            return other.__rmul__(self)
        new = self.child(other)
        new.calculate = Mul
        return new

    def __rmul__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__mul__(self)
        new = self.child(other)
        new.calculate = Mul
        return new
    
    def __truediv__(self, other):
        if isinstance(other, (list, tuple)):
            other = self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__rdiv__(self)
        new = self.child(other)
        new.calculate = rDiv
        return new

    def __rtruediv__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, metaPattern):
            return other.__div__(self)
        new = self.child(other)
        new.calculate = Div
        return new

    def __floordiv__(self, other):
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__rdiv__(self)
        new = self.child(other)
        new.calculate = rFloorDiv
        return new

    def __rfloordiv__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__div__(self)
        new = self.child(other)
        new.calculate = FloorDiv
        return new
    
    def __mod__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__rmod__(self)
        new = self.child(other)
        new.calculate = rMod
        return new
    
    def __rmod__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__mod__(self)
        new = self.child(other)
        new.calculate = Mod
        return new
    
    def __pow__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__rpow__(self)
        new = self.child(other)
        new.calculate = rPow
        return new
    
    def __rpow__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__pow__(self)
        new = self.child(other)
        new.calculate = Pow
        return new
    
    def __xor__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, metaPattern):
            return other.__rxor__(self)
        new = self.child(other)
        new.calculate = rPow
        return new
    
    def __rxor__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__xor__(self)
        new = self.child(other)
        new.calculate = Pow
        return new

    def __truediv__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__rtruediv__(self)
        new = self.child(other)
        new.calculate = rDiv
        return new
    
    def __rtruediv__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__truediv__(self)
        new = self.child(other)
        new.calculate = Div
        return new

    # Comparisons
    def __eq__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, metaPattern):
            return other.eq(self)
        new = self.child(other)
        new.calculate = lambda a, b: b.eq(a) if isinstance(b, metaPattern) else int(a == b)
        return new
    
    def __ne__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, metaPattern):
            return other.ne(self)
        new = self.child(other)
        new.calculate = lambda a, b: b.ne(a) if isinstance(b, metaPattern) else int(a != b)
        return new
    
    def __gt__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__lt__(self)
        def compare(a, b):
            value = b > a
            if isinstance(value, PGroup):
                return value
            else:
                return int(value)
        new = self.child(other)
        new.calculate = compare
        return new
    
    def __lt__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__gt__(self)
        new = self.child(other)
        def compare(a, b):
            value = b < a
            if isinstance(value, PGroup):
                return value
            else:
                return int(value)
        new.calculate = compare
        return new
    
    def __ge__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__le__(self)
        new = self.child(other)
        def compare(a, b):
            value = b >= a
            if isinstance(value, PGroup):
                return value
            else:
                return int(value)
        new.calculate = compare
        return new
    
    def __le__(self, other):
        """ If operating with a pattern, return a pattern of values """
        if isinstance(other, (list, tuple)):
            other=self.convert_to_pattern(other)
        if isinstance(other, (metaPattern, GeneratorPattern)):
            return other.__ge__(self)
        new = self.child(other)
        # a is other
        #new.calculate = lambda a, b: int(a >= b)
        def compare(a, b):
            value = b <= a
            if isinstance(value, PGroup):
                return value
            else:
                return int(value)
        new.calculate = compare
        return new

    def __abs__(self):
        new = self.child(0)
        new.calculate = lambda a, b: abs(float(b))
        return new

    def __getitem__(self, key):
        new = self.child(key)
        def getitem(a, b):
            try:
                return b[a]
            except TypeError:
                return b
        new.calculate = getitem
        return new

    def index(self, sequence):
        """ Returns a Player Key that returns the element from sequence indexed using int(self) """
        new = self.child(sequence)
        def getitem(b, a):
            try:
                return b[a]
            except TypeError:
                return b
        new.calculate = getitem
        return new

    def semitones(self):
        """ Converts the current value into the semitone value using the parent's scale """
        new = self.child(0)
        new.calculate = lambda a, b: self.parent.scale.semitones(b)
        return new

    def simple_map(self, mapping):
        """ Creates a new Player key that maps the values in the dictionary (mapping)
            to new values. Example use case:

            ```
            d1 >> play("x-o-", sample=d1.degree.simple_map( { "-" : -1, "o" : var([0,2]) }))
            ```

        """
        assert isinstance(mapping, dict)
        data = [ ((self == key) * value) for key, value in mapping.items() ]
        new_key = data[0]
        for i in data[1:]:
            new_key = new_key + i
        return new_key

    def map(self, mapping, default=0):
        """ Allows for functional mapping. `mapping` is a dictionary of keys, which can
            be functions, and values, which can also be functions. If neither is callable,
            then the the mapping function returns the value when this Player Key  is equal
            to the key. The key can be callable and will return the value provided if the
            the callable key function returns True (it must take one argument, this Player Key).
            Trivially, the following mappings are equivalent in behaviour:

            ::
                p1 >> piano(p2.degree.map({4: 7}))

                p1 >> piano(p2.degree.map({lambda x: x == 4: 7}))

            If the value is callable, then it is called on this player key when the key
            is satisfied:
            
            ::
                p1 >> piano(p2.degree.map({lambda x: x >= 4: lambda x: x + (0,2)}))
        """

        assert isinstance(mapping, dict)

        # Begin mapping
        
        funcs = {}

        for key, value in mapping.items():
            
            # We can map using a function

            if callable(key):

                key_func = lambda f: f(self.now())

            else:

                key_func = lambda v: self.now() == v

            map_key = partial(key_func, key)

            # The return value can be a function called on self.now()

            if callable(value):

                def val_func(value, func):
                    # Call on current  value (force pattern)
                    new_value = _wrapper(value).__call__(self.now()) * func()
                    
                    # Get the values from default that we want
                    def_value = (default.now() if hasattr(default, "now") else default) * _invert(func())
                    
                    return new_value + def_value

            else:

                # If we are mapping just to a single value, get the test (e.g P(1,0)) and multiply by the value

                def val_func(value, func):
                    # Call on current  value (force pattern)
                    new_value = asStream(value) * func()
                    
                    # Get the values from default that we want
                    def_value = (default.now() if hasattr(default, "now") else default) * _invert(func())
                    
                    return new_value + def_value

            map_val = partial(val_func, value, map_key)

            # Store

            funcs[map_key] = map_val

        # Is called and returns the last function that satisfies a func

        def mapping_function(*args):
            value = None
            for func, result in funcs.items():
                #if bool(func()) is True:
                #print(func(), any(asPattern(func())), "->", result())
                if recursive_any(asPattern(func())):
                    value = result()
            if value is None:
                value = default
            return value

        new = self.child(0)        
        new.calculate = mapping_function
        
        return new

    def deepmap(self, mapping, default=0):
        """ Like map, but nested values are directly mapped """

        assert isinstance(mapping, dict)

        # Begin mapping
        
        funcs = {}

        for key, value in mapping.items():
            
            # We can map using a function

            if callable(key):

                key_func = lambda f: f(self.now())

            else:

                key_func = lambda v: self.now() == v

            map_key = partial(key_func, key)

            # The return value can be a function called on self.now()

            if callable(value):

                def val_func(value, func):

                    matrix = asPattern(func())
                    
                    new_value = matrix.replace(1, _wrapper(value).__call__(self.now()))

                    def_value = (default.now() if hasattr(default, "now") else default) * _invert(matrix)
                    
                    return new_value + def_value

            else:

                # If we are mapping just to a single value, get the test (e.g P(1,0)) and multiply by the value

                def val_func(value, func):

                    matrix = asPattern(func())

                    new_value = matrix.replace(1, value)
                    
                    def_value = (default.now() if hasattr(default, "now") else default) * _invert(func())
                    
                    return new_value + def_value


            map_val = partial(val_func, value, map_key)

            # Store

            funcs[map_key] = map_val

        # Is called and returns the last function that satisfies a func

        def mapping_function(*args):
            value = None
            for func, result in funcs.items():
                #if bool(func()) is True:     
                if any(asPattern(func())):               
                    value = result()
            if value is None:
                value = default
            return value

        new = self.child(0)        
        new.calculate = mapping_function
        
        return new

    def get_min(self):
        new = self.child(0)
        def f(a, b):
            try:
                return min(b)
            except TypeError:
                return b
        new.calculate = f
        return new

    def get_max(self):
        new = self.child(0)
        def f(a, b):
            try:
                return max(b)
            except TypeError:
                return b
        new.calculate = f
        return new

    def transform(self, func):
        """ Returns a child Player Key based on the func """
        new = self.child(0)
        new.calculate = lambda a, b: func(b)
        return new

    def accompany(self, freq=0, rel=[0,2,4]):
        """ Returns a PlayerKey whose function returns an accompanying note """
        return self.transform(Accompany(freq=freq, rel=rel))

    def versus(self):
        """ e.g. `p1.pitch.versus(*rules)` """
        return
    
    # Values
    
    def __nonzero__(self):
        return self.__bool__()
    def __bool__(self):
        return bool(self.now())
    def __int__(self):
        return int(self.now())
    def __float__(self):
        return float(self.now())
    def __str__(self):
        return str(self.now())
    def __repr__(self):
        return repr(self.now())
    def __len__(self):
        return len(self.now())
    
    def __iter__(self):
        try:
            for item in self.now():
                yield item
        except TypeError:
            yield self.now()

    def child(self, other):
        return NumberKey(self.value, other)
    
    def now(self, other=None):
        """ Returns the current value in the Key by calling the parent """

        # If we have p1.degree + 2 then self.value is 2 and self.other is p1.degree
        
        if other is None:
            
            if isinstance(self.other, (NumberKey, TimeVar)):
                
                other = self.other.now()

            else:

                other = self.other

        if isinstance(self.value, (NumberKey, TimeVar)):

            value = self.value.now()

        else:

            value = self.value

        return self.calculate(value, other)

class PlayerKey(NumberKey):
    def __init__(self, value=None, reference=None, parent=None, attr=None):

        NumberKey.__init__(self, value, reference)
        
        # Reference to the Player object that is using this
        self.parent  = parent # is the player
        self.key     = attr
        self.pattern = asStream(self.parent.attr[self.key]) if self.parent is not None else asStream([])

        if reference is None:

            self.other   = 0

        else:

            self.other   = reference # is the parent Player Key -- todo: make this mroe clear
            self.parent  = reference.parent

        self.last_updated = 0

    def set(self, value, time):
        self.value = value
        self.last_updated = time
        return
    
    def update(self, value, time):
        """ Updates the contents of the PlayerKey *if* the time value is different to self.last_updated.
            If they are the same, the the contents become a PGroup of the two values """
        if not equal_values(value, self.value):
        #if value != self.value:
            if time == self.last_updated:
                try:
                    self.value.append(value)
                except AttributeError:
                    self.value = PGroup(self.value, value)
            else:
                self.value = value
        self.last_updated = time
        return

    def update_pattern(self):
        self.pattern[:] = asStream(self.parent.attr[self.key])               
        return

    def child(self, other):
        return PlayerKey(other, self, self.parent, self.key)



class Accompany:
    """ Like PlayerKey except it returns """
    def __init__(self, freq=0, rel=[0,2,4]):

        self.players_last_value = None
        self.this_last_value    = 0

        self.frequency  = freq
        self.scale_size = 7
        self.relations  = list(rel)


    def __call__(self, playerkey):
        """ Acts as a function in Player Key """
        # Only change value if the player key has changed - maybe set a frequency?
        if self.players_last_value == playerkey:
            return self.this_last_value
        else:
            return self.find_new_value(playerkey)

    def find_new_value(self, playerkey):

        # Which value is the closest to this_last_value

        values = [(playerkey + x) % 7 for x in self.relations] + [(playerkey % 7) + (x - self.scale_size) for x in self.relations]

        nearby = [abs(self.this_last_value - value) for value in values]
        
        indices = [nearby.index(val) for val in sorted(nearby)]

        r = random.random()

        if r <= 0.65:

            i = 0

        elif r <= 0.9:

            i = 1

        else:

            i = 2

        index = indices[i]

        self.this_last_value = values[index]
        self.players_last_value = playerkey
    
        return self.this_last_value
    
# class AccompanyKey(NumberKey):
#     """ Like PlayerKey except it returns """
#     def __init__(self, other, rel=[0,2,4], debug=False):

#         NumberKey.__init__(self, other, None)

#         assert(isinstance(other, PlayerKey))

#         self.parent = other.parent

#         self.last_value = self.value.now()
#         self.acmp_value = self.last_value

#         self.scale_size = 7

#         self.data       = list(rel) + [min(rel) + self.scale_size, max(rel) - self.scale_size]

#         self.debug = debug

#     def child(self, other):
#         return NumberKey(other, self)

#     def find_new_value(self, new):
#         """ Finds the item in self.data that is closest to self.acmp_value """
#         if len(self.data) == 1:
#             return self.data[0]
#         else:

#             old = self.acmp_value
            
#             A = new % self.scale_size
#             B = old % self.scale_size
            
#             # Order in "closeness" to our current value
#             shifts = sorted(self.data, key=lambda N: abs(B - (A + N)))

#             # Pick a new value to go to
#             r = random.random()

#             if r <= 0.65:

#                 i = 0

#             elif r <= 0.9:

#                 i = 1

#             else:

#                 i = 2

#             val = shifts[i]

#             return old + (val + A - B)

#     def now(self):
#         value = self.calculate(self.value.now(), self.other)
#         if isinstance(value, NumberKey):
#             value = value.now()
#         if value != self.last_value:
#             self.acmp_value = self.find_new_value(value)
#             self.last_value = value
#         return self.acmp_value


# Give pattern objects a reference to the PlayerKey type

Pattern.PlayerKey = PlayerKey

def _wrapper(f):
    """ Decorator function for forcing functions with a single value to return a Pattern object """
    def new_func(value):
        return f(asStream(value))
    return new_func

def _invert(value):
    return (value * -1) + 1