from random import choice, shuffle
from Operations import *
from Parse import Parse
from PlayString import PlayString, PlayGroup, RandomPlayGroup

"""

    metaPattern: Abstract Base Class for Pattern behaviour

"""

class metaPattern(object):
    """ Abstract base class for Patterns """

    data = None
    bracket_style = "[%s]"    

    def __init__(self, data=[]):
        
        if type(data) is str:
            
            self.fromString(data)

        elif type(data) is tuple:

            self.data = PGroup(data)
            self.make()
            
        else:
            
            self.data = data
            self.make()
            
    def __len__(self):
        lengths = [1] + [len(p) for p in self.data if isinstance(p, Pattern)]
        return LCM(*lengths) * len(self.data)
    
    def __str__(self):
        try:
            if len(self.data) > 20:
                val = self.data[:8] + [dots()] + self.data[-8:]
            else:
                val = self.data
        except AttributeError:
            val = self.data
        return "P" + self.bracket_style % repr(val)[1:-1]

    def __repr__(self):
        return str(self)

    def string(self):
        """ Returns a PlayString in string format from the Patterns values """
        string = ""
        for item in self.data:
            if isinstance(item, (PlayGroup, RandomPlayGroup)):
                string += item.string()
            elif isinstance(item, Pattern):
                string += "(" + "".join([(s.string() if hasattr(s, "string") else str(s)) for s in item.data]) + ")"
            else:
                string += str(item)
        return string

    def asGroup(self):
        return PGroup(self.data)
    
    """

        Pattern container methods
        -------------------------

    """

    # this is replaced in FoxDot.TimeVar
    def __getitem__(self, key):
        return self.getitem(key)

    def getitem(self, key):
        """ Is called by __getitem__ """
        if isinstance(key, metaPattern):
            val = self.__class__([value for n, value in enumerate(self) if key[n] > 0])
        else:
            i = key % len(self.data)
            val = self.data[i]
            if isinstance(val, (Pattern, GeneratorPattern)):
                j = key // len(self.data)
                val = val.getitem(j)
        return val
    
    def __setitem__(self, key, value):
        i = key % len(self.data)
        if isinstance(self.data[i], metaPattern):
            j = key // len(self.data)
            self.data[i][j] = value
        else:
            if key >= len(self.data):
                self.data[i] = Pattern([self.data[i], Format(value)]).stutter([key // len(self.data) , 1])
            else:
                self.data[i] = Format(value)

    def setitem(self, key, value):
        self.data[key] = Format(value)
            
    def __iter__(self):
        for i in range(len(self)):
            yield self.getitem(i)

    def items(self):
        for i, value in enumerate(self):
            yield i, value

    def __getslice__(self, start, stop, step=1):
        stop = min(stop, len(self))
        if stop < start:
            stop = (len(self.data) + start)
        return Pattern([self[i] for i in range(start, stop, step) ])
            
    def __setslice__(self, i, j, item):
        self.data[i:j] = Format(item)

    # count all values that occur?
    def count(self, item):
        return self.data.count(item)

    """

        Pattern operators (i.e. magic methods)
        --------------------------------------

    """
    def __add__(self, other):  return PAdd(self, other)
    def __radd__(self, other): return PAdd(self, other)
    def __sub__(self, other):  return PSub(self, other)
    def __rsub__(self, other): return PSub2(self, other)
    def __mul__(self, other):  return PMul(self, other)
    def __rmul__(self, other): return PMul(self, other)
    def __div__(self, other):  return PDiv(self, other)
    def __rdiv__(self, other): return PDiv2(self, other)
    def __mod__(self, other):  return PMod(self, other)
    def __rmod__(self, other): return PMod2(self, other)
    def __pow__(self, other):  return PPow(self, other)
    def __rpow__(self, other): return PPow2(self, other)
    def __xor__(self, other):  return PPow(self, other)
    def __rxor__(self, other): return PPow2(self, other)
    def __truediv__(self, other):  return PDiv(self, other)
    def __rtruediv__(self, other): return PDiv2(self, other)

    """

        Piping patterns together using the '|' operator

    """
    
    def __or__(self, other):
        """ Use the '|' symbol to 'pipe' Patterns into on another """
        return self.pipe(other)
    def __ror__(self, other):
        """ Use the '|' symbol to 'pipe' Patterns into on another """
        return asStream(other).pipe(self)
    
    #: Comparisons
    def __eq__(self, other):
        return PEq(self, other)
    def __ne__(self, other):
        return PNe(self, other)
    
    def __gt__(self, other):
        return Pattern([int(value > modi(asStream(other), i)) for i, value in enumerate(self)])
    def __ge__(self, other):
        return Pattern([int(value >= modi(asStream(other), i)) for i, value in enumerate(self)])
    def __lt__(self, other):
        return Pattern([int(value < modi(asStream(other), i)) for i, value in enumerate(self)])
    def __le__(self, other):
        return Pattern([int(value <= modi(asStream(other), i)) for i, value in enumerate(self)])

    #: Methods for strings as pattern

    def fromString(self, string):
        self.data = Parse(string)
        self.make()
        return self

    def flat(self):
        """ P.flat() -> un-nested pattern """
        new = []
        for item in self.data:
            try:
                item = item.flat()
                new += [i for i in item]
            except:
                new.append(item)
        return Pattern(new)
    
    def coeff(self):
        """ Returns a duration value relative to the type of pattern. Most patterns return val unchanged """
        return 1.0

    # Methods that return augmented versions of original

    def shuffle(self):
        new = self.__class__(self.data[:])
        shuffle(new.data)
        return new

    def reverse(self):
        new = self.__class__(self.data[:])
        new.data.reverse()
        return new
    
    def stretch(self, size):
        """ Stretches (repeats) the contents until len(Pattern) == size """
        new = []
        for n in range(size):
            new.append( modi(self.data, n) )
        new = self.__class__(new)
        return new

    def loop(self, n):
        """ Repeats this pattern n times """
        new = []
        for i in range(n):
            new += list(self)
        return self.__class__(new)

    def sort(self):
        """ Used in place of sorted(pattern) to force type """
        return self.__class__(sorted(self.data))

    def mirror(self):
        """ Reverses the pattern. Differs to `Pattern.reverse()` in that
            all nested patters are also reversed. """
        new = []
        for i in range(len(self.data), 0, -1):

            value = self.data[i-1]

            if hasattr(value, 'mirror'):

                value = value.mirror()
            
            new.append(value)
            
        return self.__class__(new)

    def swap(self, n=2):
        new = []
        for pair in [list(val) for val in [reversed(self[i:i+n]) for i in range(0, len(self), n)]]:
            for item in pair:
                new.append(item)
        return self.__class__(new)

    def splice(self, seq, *seqs):
        sequences = (self, seq) + seqs
        size = LCM(*[len(s) for s in sequences])
        new = []
        for i in range(size):
            for seq in sequences:
                new.append(seq[i])
        return self.__class__(new)

    def invert(self):
        new = []
        lrg = float(max(self.data))
        for item in self.data:
            try:
                new.append(item.invert())
            except:
                new.append((((item / lrg) * -1) + 1) * lrg)
        return self.__class__(new)

    def rotate(self, n=1):
        n = int(n)
        new = self.data[n:] + self.data[0:n]
        return self.__class__(new)

    def stutter(self, n=2):
        n = asStream(n)
        lrg = max(len(self.data), len(n))
        new = []
        for i in range(lrg):
            for j in range(modi(n,i)):
                new.append(modi(self.data,i))
        return self.__class__(new)

    def shufflets(self, n):
        """ Returns a Pattern of 'n' number of PGroups made from shuffled
            versions of the original Pattern """
        new = self.data[:]
        return Pattern([Pattern(new).shuffle().asGroup() for i in range(n)])

    def layer(self, method, *args, **kwargs):
        """ Zips a pattern with a modified version of itself. Method argument
            can be a function that takes this pattern as its first argument,
            or the name of a Pattern method as a string. """
        
        if callable(method):
            func = method
            args = [self.data] + list(args)
        else:
            func = getattr(self, method)
            assert callable(func)

        p1 = Pattern(self.data)
        p2 = Pattern(func(*args, **kwargs))

        size = LCM(len(p1), len(p2))

        data = []

        for i in range(size):

            data.append((p1[i], p2[i]))

        return Pattern(data)

    # Changing the pattern in place

    def append(self, item):
        self[len(self):] = [item]
        return self

    def i_rotate(self, n=1):
        self.data = self.data[n:] + self.data[0:n]
        return self

    def i_reverse(self):
        self.data.reverse()
        return self

    def i_sort(self):
        self.data = Pattern(sorted(self.data))
        return self

    def i_shuf(self):
        shuffle(self.data)
        return self

    def set(self, index, value):
        self.data[index] = asStream(value)
        return self

    # Boolean tests

    def contains_nest(self):
        """ Returns true if the pattern contains a nest """
        pass

    def startswith(self, prefix):
        return self.data[0] == prefix
    
    def all(self, func=(lambda x: bool(x))):
        """ Returns true if all of the patterns contents satisfies func(x) - default is nonzero """
        if len(self.data) is 0:
            return False
        
        for item in self.data:
            if not func(item):
                return False
        return True
        
    def pipe(self, pattern):
        """ Concatonates this patterns stream with another """
        data = list(self)
        for item in asStream(pattern):
            data.append(item)
        return Pattern(data)

    # Returns individual elements / slices

    def choose(self):
        """ Returns one randomly selected item """
        return choice(self.data)

    def trim(self, size):
        return self[:size]

    def ltrim(self, size):
        return self[-size:]

    # Automatic expansion of nested patterns

    def make(self):
        """ This method automatically laces and groups the data """

        #: Force data into an iterable form
        if isinstance(self.data, str):

            self.data = list(self.data)
            
        if not isinstance(self.data, (PatternType, PlayString)):
    
            self.data = [self.data]

        #: Put any data in a tuple into a PGroup
        for i, data in enumerate(self.data):
            if type(data) is tuple:
                self.data[i] = PGroup(data)
            elif type(data) is list:
                self.data[i] = Pattern(data)
            elif type(data) is str and len(data) > 1:
                self.data[i] = Pattern(data)

        self.data = list(self.data)
                
        return self

class Pattern(metaPattern):
    pass

class GeneratorPattern(object):
    """
        Used for when a Pattern does not generate a set length pattern,
        e.g. random patterns
    """
    MAX_SIZE = 2048
    def __init__(self):
        self.mod = Pattern()
        self.mod_functions = []
        self.name = self.__class__.__name__

    def __repr__(self):
        return "[GeneratorPattern <{}>]".format(self.name)
        
    def getitem(self, index):
        """ Calls self.func(index) to get an item, and also calculates
            performs any arithmetic operation assigned """
        value = self.func(index)
        for i, func in enumerate(self.mod_functions):
            value = func(value, modi(modi(self.mod, i), index))
        return value
    def func(self, index):
        return

    def __len__(self):
        return 1
    
    # Arithmetic operations create new GeneratorPatterns
    def __add__(self, other):
        return self.new(other, Add)
    def __radd__(self, other):
        return self.new(other, Add)
    def __sub__(self, other):
        return self.new(other, Sub)
    def __rsub__(self, other):
        return self.new(other, rSub)
    def __mul__(self, other):
        return self.new(other, Mul)
    def __rmul__(self, other):
        return self.new(other, Mul)
    def __div__(self, other):
        return self.new(other, Div)
    def __truediv__(self, other):
        return self.new(other, Div)
    def __rdiv__(self, other):
        return self.new(other, rDiv)
    def __rtruediv__(self, other):
        return self.new(other, rDiv)

    def new(self, other, func=Nil):
        # Create and empty GeneratorPattern
        new = GeneratorPattern()
        # Give it a list of previous mod_functions
        new.mod_functions = self.mod_functions + [func]
        # Update the base function to be the same
        new.func = self.func
        # Update it's list of modifying values
        new.mod  = Pattern([item for item in self.mod])
        new.mod.append(tuple(asStream(other)))
        return new
        
    # Container methods
    def __iter__(self):
        for i in range(self.MAX_SIZE):
            yield self[i]
    def __getitem__(self, key):
        if type(key) is int:
            return self.getitem(key)
        elif type(key) is slice:
            a = key.start if key.start else 0
            b = key.stop
            c = key.step if key.step else 1
            return Pattern([self[i] for i in range(a, b, c)])

    # Pattern methods that don't return anything
    def stretch(self, n):
        return self

class PatternContainer(Pattern):
    def getitem(self, key):
        key = key % len(self)
        return self.data[key]
    def __len__(self):
        return len(self.data)
    def __str__(self):
        return str(["%s()" % item.__class__.__name__ for item in self.data])
    def __repr__(self):
        return str(self)
    

class PGroup(metaPattern):
    """
        Class to represent any groupings of notes as denoted by brackets.
        PGroups should only be found within a Pattern object.
        
    """
    
    bracket_style = "(%s)"

    def __init__(self, data=[], *args):
        if not args:
            if isinstance(data, (PGroup, tuple)):
                data = list(data)
        else:
            data = [data] + list(args)

        metaPattern.__init__(self, data)

        # If the PGroup contains patterns, invert it to a Pattern of PGroups
        
        l = [len(p) for p in self.data if isinstance(p, Pattern)]

        if len(l) > 0:

            new_data = []

            for key in range(LCM(*l)):

                new_data.append(PGroup([item.getitem(key) if isinstance(item, Pattern) else item for item in self.data]))

            self.__class__ = Pattern

            self.data = new_data

    def getitem(self, key):
        key = key % len(self.data)        
        return self.data[key]

    def coeff(self):
        return 0.5

    def scale_dur(self, n):
        """ Scales the dur values for all the items in self.data by n """
        for item in self.data:
            item.scale_dur(n)
        return

    def fromString(self, string):
        metaPattern.fromString(self, string)
        self.scale_dur(self.coeff())
        return self

    def merge(self, value):
        """ Merge values into one PGroup """
        if hasattr(value, "__len__"):
            new_data = list(value)
        else:
            new_data = [value]
        return PGroup(list(self.data) + new_data)
            

Pgroup = PGroup #: Alias for PGroup

class Shared_Time_PGroup(PGroup):
    bracket_style = "{%s}"
    def coeff(self):
        return 1.0 / len(self)


# Functions used to separate Groups and Nests from within Patterns

##def nested(data):
##    """ Returns true is data is any kind of pattern (inc. lists) EXCEPT PGroups or TimeVars """
##    try:
##        return data.NEST_ME
##    except:
##        return isinstance(data, list)

##def contains_nest(data):
##    """ Returns true if any items in data are 'nest-able' patterns """
##    try:
##        return any([nested(item) for item in data])
##    except:
##        return False
##
##def Place(data):
##    """ nested patterns are stretched
##        e.g. [[1,0],0,1,0] would be returned as [1,0,1,0,0,0,1,0] """
##
##    if contains_nest(data):
##
##        #: Works out the largest sub-patterns and loops the overall pattern until it is stretched out
##        
##        sub = LCM(*[len(item) for item in data if nested(item)])
##        new = []
##
##        for i in range( sub ):
##            for j in range(len(data)):
##                item = data[j]
##                if nested(item):
##                    item = modi(item, i)
##                    if type(item) is tuple:
##                        item = PGroup(item)
##                new.append(item)
##        return new
##    
##    else:
##         #: If the pattern doesn't need lacing, return original
##        return data


# Used to force any non-pattern data into a Pattern

PatternType = (Pattern, list)
                
def asStream(data):
    """ Forces any data into a [pattern] form """
    if isinstance(data, (Pattern, GeneratorPattern)):
        return data
    return Pattern(data)

def Format(data):
    if isinstance(data, list):
        return Pattern(data)
    if isinstance(data, tuple):
        return PGroup(data)
    return data

def Dominant(*patterns):
    for p in patterns:
        if isinstance(p, (Pattern, list)):
           return Pattern 
    return PGroup      

def Convert(*args):
    """ Returns tuples/PGroups as PGroups, and anything else as Patterns """
    PatternTypes = []
    for val in args:
        if isinstance(val, (Pattern, PGroup)):
            PatternTypes.append(val)
        elif isinstance(val, tuple):
            PatternTypes.append(PGroup(val))
        else:
            PatternTypes.append(Pattern(val))
    return PatternTypes if len(PatternTypes) > 0 else PatternTypes[0]

class dots:        
    """ Class for representing long Patterns in strings """
    def __repr__(self):
        return '...'
