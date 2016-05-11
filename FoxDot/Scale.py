from Patterns.Base import Pattern

def directory():

    return scale_types.keys()

def Object():

    return 

class Scale(Pattern):

    def __init__(self, data=None):

        if data is None:

            self.data = major

        else:

            if type(data) is str:

                self.data = scale_types[data]

            else:

                self.data = data

    def __call__(self, *args):

        if len(args) > 0:

            self.change(args[0])

        return self

    def __eq__(self, other):

        return other == Object

    def __ne__(self, other):

        return other != Object

    def change(self, new):

        if type(new) == str:

            self.data = scale_types[new]

        elif type(new) == list:

            self.data = new

        return self

#: Define scales

chromatic       = Scale([0,1,2,3,4,5,6,7,8,9,10,11,12])
major           = Scale([0,2,4,5,7,9,11])
majorPentatonic = Scale([0,2,4,7,9])
minor           = Scale([0,2,3,5,7,8,10])
minorPentatonic = Scale([0,3,5,7,10])
mixolydian      = Scale([0,2,4,5,7,9,10])
melodicMinor    = Scale([0,2,3,5,7,9,11])
harmonicMinor   = Scale([0,2,3,5,7,8,11])
justMajor       = Scale([ 0, 2.0391000173077, 3.8631371386483, 4.9804499913461, 7.0195500086539, 8.8435871299945, 10.882687147302 ])
justMinor       = Scale([ 0, 2.0391000173077, 3.1564128700055, 4.9804499913461, 7.0195500086539, 8.1368628613517, 10.175962878659 ])

# Custom made fibonacci tuning

fib = [0,1]
for n in range(2,11):
    fib.append(fib[n-1]+fib[n-2])

    
fibonacci = []
for n in range(3, len(fib)-1):
    fibonacci.append((n-3) * (fib[n] / float(fib[n-1])))   

scale_types = { "chromatic"         : chromatic,
                "major"             : major,
                "minor"             : minor,
                "mixolydian"        : mixolydian,
                "melodicMinor"      : melodicMinor,
                "harmonicMinor"     : harmonicMinor,
                "majorPentatonic"   : majorPentatonic,
                "minorPentatonic"   : minorPentatonic,
                "justMajor"         : justMajor,
                "justMinor"         : justMinor,
                "fibonacci"         : fibonacci }


default = Scale("major")  
