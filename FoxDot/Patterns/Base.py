from random import choice
from Operations import *
from ..Code.parse import brackets, closing_brackets

class metaPattern(object):
    """
        Abstract pattern class
        ======================
        
    """

    data = None

    def __init__(self, data=[]):
        
        if type(data) is str:
            
            self.fromString(data)
            
        else:
            
            self.data = data
            self.make()
            
    def __len__(self):
        return len(self.data)
    def __str__(self):
        return self.BRACKETS % str(self.data)[1:-1]
    def __repr__(self):
        return str(self)
    def string(self):
        """ Returns a string made up of all the values:

            PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" """
        string = ""
        for item in self.data:
            try:
                string += item.string()
            except:
                string += str(item)
        return string
    #: Container methods
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __iter__(self):
        for data in self.data:
            yield data
    def __getslice__(self, i, j):
        return Pattern( self.data[i:j] )
    def __setslice__(self, i, j, item):
        self.data[i:j] = item
    #: Operators
    def __add__(self, other):
        return PAdd(self, other)
    def __radd__(self, other):
        return PAdd(self, other)
    def __sub__(self, other):
        return PSub(self, other)
    def __rsub__(self, other):
        return PSub(other, self)
    def __mul__(self, other):
        return PMul(self, other)
    def __rmul__(self, other):
        return PMul(other, self)
    def __truediv__(self, other):
        return PDiv(self, other)
    def __rtruediv__(self, other):
        return PDiv(other, self)
    def __div__(self, other):
        return PDiv(self, other)
    def __rdiv__(self, other):
        return PDiv(other, self)
    def __mod__(self, other):
        return PMod(self, other)
    def __rmod__(self, other):
        return PMod(other, self)
    def __pow__(self, other):
        return PPow(self, other)
    def __rpow__(self, other):
        return PPow(other, self)
    def __xor__(self, other):
        return PPow(self, other)
    def __rxor__(self, other):
        return PPow(other, self)
    #: Piping patterns
    def __or__(self, other):
        """ Use the '|' symbol to 'pipe' Patterns into on another """
        return Pattern(self.pipe(other))
    def __ror__(self, other):
        """ Use the '|' symbol to 'pipe' Patterns into on another """
        return Pattern(asStream(other).pipe(self))
    #: Comparisons
    def __eq__(self, other):
        try:
            return self.data == other.data
        except:
            return self.data == other

    def __ne__(self, other):
        try:
            return self.data != other.data
        except:
            return self.data != other

    #: Non-Python special methods
    def fromString(self, string):
        """
            Used to convert a string of characters into a pattern, either 

            Characters can be PGrouped in brackets and each group have their
            own set of behaviours.

            Half-Time Groups
            ----------------

            [] - Puts the characters into Half_Time_PGroups

            Laced Groups
            ------------

            () - Put into a list and become nested

            Shared-Time Groups
            ------------------

            {} - Put into a Single_Time_PGroup 

            Rather unintuitively: Characters in square brackets, [], are
            placed in a tuple - and then become PGroups - and characters
            in round brackets, (), are added into a nested list

            "x-o(-[oo])" -> ["x","-","o","-","x","-","o",("o","o")]
        
        """

        i = 0
        self.data = []
        
        bracket_styles = {"()" : Pattern,
                          "[]" : PGroup,
                          "{}" : Shared_Time_PGroup }

        while i < len(string):

            char = string[i]

            if char in "([{":
                
                a, b = brackets(string, i, closing_brackets[char])

                char = bracket_styles[string[a]+string[b-1]](string[a+1:b-1])

                i = b - 1

            self.data.append(char)

            i += 1

        self.make()
            
        return self
    
    def dur(self, val):
        """ Returns a duration value relative to the type of pattern. Most patterns return val unchanged """
        return val               
                
        return PGroup([val for x in self])
    def contains_nest(self):
        """ Returns true if the pattern contains a nest """
        pass
    def stretch(self, size):
        """ Stretches (repeats) the contents until len(Pattern) == size """
        new = []
        for n in range(size):
            new.append( modi(self.data, n) )
        self.data = new
        return self

    def startswith(self, prefix):
        return self.data[0] == prefix

    def copy(self):
        new = self.data
        return self.__class__(new)
    
    def items(self):
        for i, data in enumerate(self.data):
            yield i, data
    
    def all(self, func=(lambda x: bool(x))):
        """ Returns true if all of the patterns contents satisfies func(x) - default is nonzero """
        if len(self.data) is 0:
            return False
        
        for item in self.data:
            if not func(item):
                return False
        return True

    def append(self, item):
        self[len(self):] = [item]
        #self.data.append(item)
        return self
        
    def pipe(self, pattern):
        """ Concatonates this patterns stream with another """
        data = list(self)
        for item in pattern:
            data.append(item)
        return self.__class__(data)

    def loop(self, n):
        """ Repeats this pattern n times """
        data = []
        for i in range(n):
            data += list(self)
        return self.__class__(data)

    def sort(self):
        """ Used in place of sorted(pattern) to force type """
        return self.__class__(sorted(self.data))

    def choose(self):
        """ Returns one randomly selected item """
        return choice(self.data)

    def make(self):
        """ This method automatically laces and groups the data """

        #: Force data into an iterable form
        if isinstance(self.data, str):

            self.data = list(self.data)
            
        if not isinstance(self.data, list):
    
            self.data = [self.data]

        #: Put any data in a tuple into a PGroup
        for i, data in enumerate(self.data):
            if type(data) is tuple:
                self.data[i] = PGroup(data)

        #: Lace any nested lists
        self.data = Place(self.data)
        
        return self

class Pattern(metaPattern):
    """
        Pattern Base Class
        ==================
        
    """

    NEST_ME = True
    BRACKETS = "[%s]"

    

class PGroup(metaPattern):
    """
        Class to represent any groupings of notes as denoted by brackets.
        PGroups should only be found within a Pattern object.
        
    """

    NEST_ME = False
    BRACKETS = "(%s)"
    
    def make(self):
        """
            Overrides the Pattern.make() method to allow PGroup to invert nesting:

            i.e. (0,[1,2]) -> [(0,1),(0,2)] and NEST_ME flag is set to False
            i.e. (0,[1,2],[3,4]) -> [(0,1,3),(0,2,4)]

        """

        #: Inverts the nested and grouped data if PGroup has a nested Pattern
        if contains_nest(self.data):
            
            sub = Place(self.data)

            step = len(self.data)

            self.data = [PGroup(sub[n:n+step]) for n in range(0, len(sub), step)]

            # Make this a pseudo-normal pattern          
            self.NEST_ME = True
            
        return self

    def dur(self, val):
        return val * 0.5

Pgroup = PGroup #: Alias for PGroup

class Shared_Time_PGroup(PGroup):
    def dur(self, val):
        return val / len(self)


# Functions used to separate Groups and Nests from within Patterns

def nested(data):
    """ Returns true is data is any kind of pattern (inc. lists) EXCEPT PGroups or TimeVars """
    try:
        return data.NEST_ME
    except:
        return isinstance(data, list)

def contains_nest(data):
    """ Returns true if any items in data are 'nest-able' patterns """
    try:
        return any([nested(item) for item in data])
    except:
        return False

def Place(data):
    """ nested patterns are stretched
        e.g. [[1,0],0,1,0] would be returned as [1,0,1,0,0,0,1,0] """

    if contains_nest(data):

        #: Works out the largest sub-patterns and loops the overall pattern until it is stretched out
        
        sub = max([len(item) for item in data if nested(item)])
        new = []

        for i in range( sub ):
            for j in range(len(data)):
                item = data[j]
                if nested(item):
                    item = modi(item, i)
                    if type(item) is tuple:
                        item = PGroup(item)
                new.append(item)
        return new
    
    else:
         #: If the pattern doesn't need lacing, return original
        return data


# Used to force any non-pattern data into a Pattern

def asStream(data):
    """ Forces any data into a pattern form """
    if isinstance(data, Pattern):
        return data
    return Pattern(data)

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
    return PatternTypes
