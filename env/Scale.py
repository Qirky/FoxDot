chromatic   = range(12)

major           = [0,2,4,5,7,9,11]
majorPentatonic = [0,2,4,7,9]
minor           = [0,2,3,5,7,8,10]
minorPentatonic = [0,3,5,7,10]
mixolydian      = [0,2,4,5,7,9,10]
melodicMinor    = [0,2,3,5,7,9,11]
harmonicMinor   = [0,2,3,5,7,8,11]
justMajor       = [ 0, 2.0391000173077, 3.8631371386483, 4.9804499913461, 7.0195500086539, 8.8435871299945, 10.882687147302 ]
justMinor       = [ 0, 2.0391000173077, 3.1564128700055, 4.9804499913461, 7.0195500086539, 8.1368628613517, 10.175962878659 ]

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

def directory():

    return scale_types.keys()

class Scale:

    def __init__(self, s=None):

        self.__type__ = "scale"

        if not s:

            self.steps = major

        else:

            if type(s) == str:

                self.steps = scale_types[s]

            else:

                self.steps = s

    def __len__(self):

        return len(self.steps)

    def __str__(self):

        return str(self.steps)

    def __iter__(self):

        for item in self.steps:

            yield item

    def __getitem__(self, key):

        return self.steps[key]

    def change(self, new):

        if type(new) == str:

            self.steps = scale_types[new]

        elif type(new) == list:

            self.steps = new

        return self

        
