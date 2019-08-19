from __future__ import absolute_import, division, print_function

from .Patterns import *
from .TimeVar import TimeVar
from .Utils import recursive_any, get_inverse_op
from functools import partial

def convert_to_pattern(value):
    if isinstance(value,  list):
        value = Pattern(value)
    elif isinstance(value, tuple):
        value = PGroup(value)
    elif not isinstance(value, metaPattern):
        value = Pattern(value)
    return value

def convert_pattern_args(func):
    def new_method(self, value):
        if isinstance(value, (list, tuple)):
            value = convert_to_pattern(value)
        # if isinstance(value, (metaPattern, GeneratorPattern)):
        if isinstance(value, (Pattern, GeneratorPattern)):
            other_op = get_inverse_op(func.__name__)
            return getattr(value, other_op).__call__(self)
        return func(self, value)
    return new_method


class NumberKey(object):
    """ An object that acts like a number but may have dependencies when returing its
        value. These are used when returing Player object attribute values accessed via
        `getattr` e.g. `p1.dur` or `getattr(p1, "dur")`. The parent attribute is the Player
        that contains the key or the referenced key in the case that the value has been
        maniupulated. e.g. if `p1` is using `p2.degree` then `p1.degree.parent == p1` and 
        `p1.degree.value.parent == p2`.
    """

    def __init__(self, value=0, function=None):
        # the number to store/update
        self.value     = value
        self.calculate = function if function is not None else lambda x: x
        # reference to another number key that this is linked to
        # self.other = reference
        # self.parent = self.value if isinstance(self.value, NumberKey) else None
        # This is the Player object whose attribute this is fetching / chained to
        # self.parent = self.other.parent if isinstance(self.other, NumberKey) else None
        # self.

    def parent(self):
        return self.value if isinstance(self.value, NumberKey) else None

    def get_root(self):
        child = self
        while True:
            parent = child.parent() 
            if parent is None:
                break
            child = parent
        return child

    def path_to_root(self):
        child = self
        while True:
            parent = child.parent()
            if parent is None:
                break
            child = parent
            yield child


    def has_circular_reference(self):
        return self in self.path_to_root()

    def is_root(self):
        return self.parent() is None

    # Storing mathematical operations
    
    @convert_pattern_args
    def __add__(self, other):
        function = lambda value: value + other
        return self.transform(function)

    @convert_pattern_args
    def __radd__(self, other):
        function = lambda value: other + value
        return self.transform(function)

    @convert_pattern_args
    def __sub__(self, other):
        function = lambda value: value - other
        return self.transform(function)

    @convert_pattern_args
    def __rsub__(self, other):
        function = lambda value: other - value
        return self.transform(function)
    
    @convert_pattern_args
    def __mul__(self, other):
        function = lambda value: value * other
        return self.transform(function)

    @convert_pattern_args
    def __rmul__(self, other):
        function = lambda value: other * value
        return self.transform(function)

    @convert_pattern_args
    def __truediv__(self, other):
        function = lambda value: value / other
        return self.transform(function)

    @convert_pattern_args
    def __rtruediv__(self, other):
        function = lambda value: other / value
        return self.transform(function)

    @convert_pattern_args
    def __floordiv__(self, other):
        function = lambda value: value // other
        return self.transform(function)

    @convert_pattern_args
    def __rfloordiv__(self, other):
        function = lambda value: other // value
        return self.transform(function)
    
    @convert_pattern_args
    def __mod__(self, other):
        function = lambda value: value % other
        return self.transform(function)

    @convert_pattern_args
    def __rmod__(self, other):
        function = lambda value: other % value
        return self.transform(function)
    
    @convert_pattern_args
    def __pow__(self, other):
        """ If operating with a pattern, return a pattern of values """
        function = lambda value: value ** other
        return self.transform(function)
    
    @convert_pattern_args
    def __rpow__(self, other):
        """ If operating with a pattern, return a pattern of values """
        function = lambda value: value ** other
        return self.transform(function)
    
    @convert_pattern_args
    def __xor__(self, other):
        """ If operating with a pattern, return a pattern of values """
        function = lambda value: value ** other
        return self.transform(function)
    
    @convert_pattern_args
    def __rxor__(self, other):
        """ If operating with a pattern, return a pattern of values """
        function = lambda value: other ** value
        return self.transform(function)

    @convert_pattern_args
    def __eq__(self, other):
        function = lambda value: value == other
        return self.transform(function)
    
    @convert_pattern_args
    def __ne__(self, other):
        function = lambda value: (value != other)
        return self.transform(function)

    @convert_pattern_args
    def __gt__(self, other):
        function = lambda value: (value > other)
        return self.transform(function)

    @convert_pattern_args
    def __ge__(self, other):
        function = lambda value: (value >= other)
        return self.transform(function)

    @convert_pattern_args
    def __lt__(self, other):
        function = lambda value: (value < other)
        return self.transform(function)

    @convert_pattern_args
    def __le__(self, other):
        function = lambda value: (value <= other)
        return self.transform(function)

    def __abs__(self):
        return self.transform(abs)

    def __getitem__(self, key):
        def function(value):
            try:
                return value[key]
            except TypeError:
                return value
        return self.spawn_child(function)

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
        
        # input functions
        functions = []
    
        # Convert default output to function
        if callable(default):
            default_func = default
        else:
            default_func = partial(lambda x, y: x, default)
        
        # Convert input values to functions
        for key, value in mapping.items():
            if callable(key):
                test_func = force_pattern_args(key)
            else:
                test_func = partial(lambda x, y: x == y, key)
            
            if callable(value):
                result_func = force_pattern_args(value)
            else:
                result_func = partial(lambda x, y: x, value)
                
            functions.append((test_func, result_func))
            
        # Define mapping function to test input functions
        def mapping_function(value):
            # For PGroups
            if isinstance(value, PGroup):
                return PGroup([mapping_function(item) for item in value])

            # For other values
            for func, result in functions:
                if bool(func(value)) is True:
                    return result(value)
            return default_func(value)

        return self.spawn_child(mapping_function)

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
        """ Returns a child Player Key based on the func. If the value
            returned is a PGroup, that is also transformed by the function """
        # def new_func(item):
        #     if isinstance(item, (PGroup, Pattern)):
        #         return item.transform(func)
        #     else:
        #         return func(item)
        def new_func(item):
            try:
                return func(item)
            except AttributeError as e:
                error = e
            try:
                return item.transform(func)
            except AttributeError:
                # Raise original error for more information
                raise error

        return self.spawn_child(new_func)

    def accompany(self, rel=[0,2,4]):
        """ Returns a PlayerKey whose function returns an accompanying note """
        return self.transform(Accompany(rel=rel))

    def versus(self, rule=lambda x, y: x > y):
        """ p1 >> pads([0, 1, 2, 3])
            p2 >> pluck([4, 5, 0]).versus(p1, rule)
        """
        
        # 1. Sets this source player key amplify to be "off" when the rule is satisfied

        # 2. Returns a new PlayKey

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

    # def child(self, other):
    #     return NumberKey(self.value, other)

    def spawn_child(self, function):
        return self.__class__(self, function)
    
    def now(self, other=None):
        """ Returns the current value in the Key by calling the parent """

        value = self.value.now() if hasattr(self.value, "now") else self.value

        return self.calculate(value)

class PlayerKey(NumberKey):
    # def __init__(self, value=None, reference=None, parent=None, attr=None):
    def __init__(self, value, function=None, player=None, attr=None):

        NumberKey.__init__(self, value, function)

        if player is None and isinstance(self.value, PlayerKey):

            self.attr   = self.value.attr
            self.player = self.value.player

        else:

            self.attr    = attr
            self.player = player

        # self.pattern = asStream(self.parent.attr[self.key]) if self.parent is not None else asStream([]) #
        # self.pattern = NumberKey().transform(lambda x: self.player.attr[self.attr])

        self.last_updated = 0

    def cmp(self, player, attr):
        return player == self.player and attr == self.attr

    def get_player_attribute(self):
        return self.player.attr[self.attr]

    def name(self):
        return "{}.{}".format(self.player.id, self.attr)

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

    # Could be removed
    def update_pattern(self):
        # try:
        #     self.pattern[:] = asStream(self.parent.attr[self.key])
        # except TypeError:
        #     self.pattern = asStream(self.parent.attr[self.key])
        return


class Accompany:
    """ Like PlayerKey except it returns """
    this_last_value = 0
    keys_last_value = None

    def __init__(self, rel=[0,2,4]):

        # self.frequency  = freq
        self.scale_size = 7
        self.relations  = list(rel)

    def __call__(self, playerkey):
        """ Acts as a function in Player Key """
        # Only change value if the player key has changed - maybe set a frequency?
        if self.keys_last_value != playerkey:
            self.this_last_value = self.find_new_value(playerkey)
            self.keys_last_value = playerkey
        return self.this_last_value

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

        index = indices[i % len(indices)]

        return values[index]

class Versus(Accompany):
    def __init__(self):
        pass
    def find_new_value(self, playerkey):
        return 


# Give pattern objects a reference to the PlayerKey type

Pattern.PlayerKey = PlayerKey