from random import choice
from Operations import *

class Pattern(list):
    """
        Abstract pattern class. 
        
    """

    NEST_ME = True
    BRACKETS = "[%s]"

    def __init__(self, data):

        #: Forces data to be iterable and mutable
        if not isinstance(data, (list, str)):
            data = [data]

        self.data = data
        self.make()
        
    def __len__(self):
        return len(self.data)
    
    #: Conversions
    def __str__(self):
        if self.all(lambda a: type(a) is str):
            return "".join(self.data)
        else:
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
    def list(self):
        return [item for item in self.data]
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
        """ Circular / Vector add 2 Patterns """
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

    def fromString(self, string):
        """
            Used to convert a string of characters into a pattern.

            Rather unintuitively: Characters in square brackets, [], are
            placed in a tuple - and then become PGroups - and characters
            in round brackets, (), are added into a nested list

            "x-o(-[oo])" -> ["x","-","o","-","x","-","o",("o","o")]
        
        """

        self.data = []
        
        if type(string) != str:
            raise TypeError("Argument must be a string")

        # Loop through string

        inGroup = False
        inNest = False

        chunks = {}
        chunks['group'] = []
        chunks['nest']  = []
        chunks['last']  = None

        for char in string:
            if char is "[" :
                inGroup = True
                chunks['last'] = 'group'
            elif char is "(":
                inNest = True
                chunks['last'] = 'nest'
            elif char is "]":
                
                if inGroup:
                    if inNest:
                        chunks['nest'].append(tuple(chunks['group']))
                    else:
                        self.data.append(tuple(chunks['group']))
                    inGroup = False
                    chunks['group'] = []
                    
            elif char is ")":
                
                if inNest:
                    if inGroup:
                        chunks['group'].append(chunks['nest'])
                    else:
                        self.data.append(chunks['nest'])
                    inNest = False
                    chunks['nest'] = []

            elif inGroup and inNest:

                chunks[chunks['last']].append(char)

            elif inGroup:
                chunks['group'].append(char)

            elif inNest:
                chunks['nest'].append(char)

            else:
                self.data.append(char)

        self.make()
        
        return self

    def copy(self):
        new = self.data
        return Pattern(new)
    
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
        data = self.list()
        for item in pattern:
            data.append(item)
        return Pattern(data)

    def loop(self, n):
        """ Repeats this pattern n times """
        data = []
        for i in range(n):
            data += self.list()
        return Pattern(data)

    def sorted(self):
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

class PGroup(Pattern):
    """
        Class to represent any groupings of notes as denoted by brackets
    """

    NEST_ME = False
    BRACKETS = "(%s)"
    
    def __init__(self, data):
        self.data = data
        self.make()
    def __repr__(self):
        return str(self)
    def copy(self):
        """ Returns a new PGroup with self.data """
        new = self.data
        return PGroup(new)
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

Pgroup = PGroup #: Alias for PGroup


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
