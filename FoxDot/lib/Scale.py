from Patterns.Main import Pattern
from random import choice

def choose():
    """ Scale.choose() -> Returns a random scale object """
    return choice(Scale.names.values())
    

class ScalePattern(Pattern):

    names = {}
    name  = 'unnamed'

    def __init__(self, name, *args):

        self.name = name

        if args:

            ScalePattern.names[name] = self.data = args[0]

        else:

            self.data = ScalePattern.names[name]

        self.pentatonic = PentatonicScalePattern(self)

    def __call__(self, *args):

        if len(args) > 0:

            self.set(args[0])

        return self

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, ScalePattern) else False

    def __ne__(self, other):
        return self.name != other.name if isinstance(other, ScalePattern) else True

    def set(self, new):

        if new is self:

            return self

        if type(new) == str:

            self.data = self.__class__.names[new]
            self.name = new

        elif isinstance(new, (list, Pattern)):

            self.data = new
            self.name = self.__class__.name

        else:

            print "Warning: {} is not a valid scale".format(new)       

        return self
        

class PentatonicScalePattern(ScalePattern):

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
    def __repr__(self):
        return "[inf]"


# Custom made fibonacci tuing

##fib = [0,1]
##for n in range(2,11):
##    fib.append(fib[n-1]+fib[n-2])
##    
##fibonacci = []
##for n in range(3, len(fib)-1):
##    fibonacci.append((n-3) * (fib[n] / float(fib[n-1])))
##
##fibonacci = Scale("fibonacci", fibonacci)
##
##del n

# Default scale is major

class __scale__:

    chromatic       = ScalePattern("chromatic", [0,1,2,3,4,5,6,7,8,9,10,11,12])

    major           = ScalePattern("major", [0,2,4,5,7,9,11])
    majorPentatonic = ScalePattern("majorPentatonic", [0,2,4,7,9])

    minor           = ScalePattern("minor", [0,2,3,5,7,8,10])
    minorPentatonic = ScalePattern("minorPentatonic", [0,3,5,7,10])

    mixolydian      = ScalePattern("mixolydian", [0,2,4,5,7,9,10])

    melodicMinor    = ScalePattern("melodicMinor", [0,2,3,5,7,9,11])
    melodicMajor    = ScalePattern("melodicMinor", [0,2,4,5,7,8,11])

    harmonicMinor   = ScalePattern("harmonicMinor", [0,2,3,5,7,8,11])
    harmonicMajor   = ScalePattern("harmonicMajor", [0,2,4,5,7,8,11])

    #justMajor       = ScalePattern("justMajor", [ 0, 2.0391000173077, 3.8631371386483, 4.9804499913461, 7.0195500086539, 8.8435871299945, 10.882687147302 ])
    #justMinor       = ScalePattern("justMinor", [ 0, 2.0391000173077, 3.1564128700055, 4.9804499913461, 7.0195500086539, 8.1368628613517, 10.175962878659 ])

    dorian          = ScalePattern("dorian", [0,2,3,5,7,9,10])

    egyptian        = ScalePattern("egyptian", [0,2,5,7,10])
    zgi             = ScalePattern("zhi", [0,2,5,7,9])
    phyrgian        = ScalePattern("phrygian", [0,1,3,5,7,8,10])
    prometheus      = ScalePattern("prometheus", [0,2,4,6,11])
    indian          = ScalePattern("indian", [0,4,5,7,10])

    locrian         = ScalePattern("locrian", [0,1,3,5,6,8,10])
    locrianMajor    = ScalePattern("locrianMajor", [0,2,4,5,6,8,10])

    lydian          = ScalePattern("lydian", [0,2,4,6,7,9,11])
    lydianMinor     = ScalePattern("lydianMinor", [0,2,4,6,7,8,10])

    freq            = ScalePattern("freq", _freq())

    def __init__(self):

        self.default = ScalePattern("major")
        
    def __setattr__(self, key, value):
        if key == "default" and key in vars(self):
            self.default.set(value)
        else:
            self.__dict__[key] = value
        return

    @staticmethod
    def names():
        """ Returns a list of all the scales by name """
        return sorted(ScalePattern.names.keys())


Scale = __scale__()
