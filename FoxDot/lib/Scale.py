from Patterns.Base import Pattern
from random import choice

def names():
    """ Returns a list of all the scales by name """
    return sorted(Scale.names.keys())

def choose():
    """ Scale.choose() -> Returns a random scale object """
    return choice(Scale.names.values())
    

class Scale(Pattern):

    names = {}
    name  = 'unnamed'

    def __init__(self, name, *args):

        self.name = name

        if args:

            self.__class__.names[name] = self.data = args[0]

        else:

            self.data = Scale.names[name]

        self.pentatonic = PentatonicScale(self)

    def __call__(self, *args):

        if len(args) > 0:

            self.set(args[0])

        return self

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, Scale) else False

    def __ne__(self, other):
        return self.name != other.name if isinstance(other, Scale) else True

    def set(self, new):

        if new is self:

            return self

        if type(new) == str:

            self.data = self.__class__.names[new]
            self.name = new

        elif isinstance(new, (list, Pattern)):

            self.data = new
            self.name = Scale.name

        else:

            print "Warning: {} is not a valid scale".format(new)       

        return self

    def __rshift__(self, other):
        return self.set(other)
        

class PentatonicScale(Scale):

    def __init__(self, scale):

        self.data = scale

    def __len__(self):
        return 5

    @staticmethod
    def values(scale):

        shift = ((scale[2]-scale[0]) % 2) * 2

        return sorted([scale[(i+shift)%len(scale)] for i in range(0,5*4,4)])

    def __str__(self):
        return str(self.values(self.data))

    def __repr__(self):
        return str(self)

    def __iter__(self):

        for note in self.values(self.data):

            yield note

    def __getitem__(self, key):

        return self.values(self.data)[key]

class _freq:
    def __str__(self):
        return "[inf]"

#: Define scales

chromatic       = Scale("chromatic", [0,1,2,3,4,5,6,7,8,9,10,11,12])

major           = Scale("major", [0,2,4,5,7,9,11])
majorPentatonic = Scale("majorPentatonic", [0,2,4,7,9])

minor           = Scale("minor", [0,2,3,5,7,8,10])
minorPentatonic = Scale("minorPentatonic", [0,3,5,7,10])

mixolydian      = Scale("mixolydian", [0,2,4,5,7,9,10])

melodicMinor    = Scale("melodicMinor", [0,2,3,5,7,9,11])
melodicMajor    = Scale("melodicMinor", [0,2,4,5,7,8,11])

harmonicMinor   = Scale("harmonicMinor", [0,2,3,5,7,8,11])
harmonicMajor   = Scale("harmonicMajor", [0,2,4,5,7,8,11])

#justMajor       = Scale("justMajor", [ 0, 2.0391000173077, 3.8631371386483, 4.9804499913461, 7.0195500086539, 8.8435871299945, 10.882687147302 ])
#justMinor       = Scale("justMinor", [ 0, 2.0391000173077, 3.1564128700055, 4.9804499913461, 7.0195500086539, 8.1368628613517, 10.175962878659 ])

dorian          = Scale("dorian", [0,2,3,5,7,9,10])

egyptian        = Scale("egyptian", [0,2,5,7,10])
zgi             = Scale("zhi", [0,2,5,7,9])
phyrgian        = Scale("phrygian", [0,1,3,5,7,8,10])
prometheus      = Scale("prometheus", [0,2,4,6,11])
indian          = Scale("indian", [0,4,5,7,10])

locrian         = Scale("locrian", [0,1,3,5,6,8,10])
locrianMajor    = Scale("locrianMajor", [0,2,4,5,6,8,10])

lydian          = Scale("lydian", [0,2,4,6,7,9,11])
lydianMinor     = Scale("lydianMinor", [0,2,4,6,7,8,10])

freq            = Scale("freq", _freq())

# Custom made fibonacci tuning

fib = [0,1]
for n in range(2,11):
    fib.append(fib[n-1]+fib[n-2])
    
fibonacci = []
for n in range(3, len(fib)-1):
    fibonacci.append((n-3) * (fib[n] / float(fib[n-1])))

del n

fibonacci = Scale("fibonacci", fibonacci)

# Default scale is major

default = Scale("major")  
