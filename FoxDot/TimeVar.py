from Patterns import Place, GeomFill, modi, Stretch

# Function that does a similar job to Players.asStream but stops the rec
def asStream(data):
    """ Returns data as a list """
    if type(data) not in (list, tuple):

        data = [data]

    return Place(data)

# Used to determine if an instance is timevar
def Object():
    return

def InfinityObj():
    return

class TimeVar:

    def __init__(self, values, dur=4, metro=None):

        self.metro  = metro
        self.data   = values
        self.dur    = dur
        
        self.has_inf = False
        self.inf     = False
        self.inf_val = None
        
        self.update(values, dur)

    def __str__(self):

        return str(self.now())

    def __len__(self):

        try:

            return len(self.now())

        except:

            return 1

    def __int__(self):

        return int(self.now())

    def __add__(self, n):

        return TimeVar([val[0]+n for val in self.data], self.dur)

    def __sub__(self, n):

        return TimeVar([val[0]-n for val in self.data], self.dur)

    def __float__(self):

        return float(self.now())

    def __eq__(self, other):

        return other == self.now()

    def __ne__(self, other):

        return other != self.now()

    def __iter__(self):

        try:

            for x in self.now():

                yield x

        except:

            yield self.now()

    def length(self):
        return self.data[-1][2] + 1

    def update(self, values, dur=None):
        """ Updates the TimeVar with new values """

        if dur is not None:
            self.dur=asStream(dur)

        if InfinityObj in self.dur:
            if self.dur[-1] != InfinityObj:
                raise
            else:
                self.has_inf = True

        self.data = []
        a, b = 0, -1

        for i, val in enumerate(asStream(values)):

            if isinstance(modi(self.dur,i), _infinity):

                # Replace infinity with a reasonable amount of time
                
                this_dur = GeomFill(Stretch(self.dur, i))[-1]
                
            else:

                # Get the duration for this value
                
                this_dur = modi(self.dur, i)

            a = b + 1
            b = a + (self.metro.steps * this_dur) - 1
    
            self.data.append((val, a, b))

        return

    def now(self):
        """ Returns the value from self.val for time t in self.metro """

        if self.inf:
            return self.inf_value

        t = self.metro.now() % self.length()

        for i in range(len(self.data)):
            
            if self.data[i][1] <= t <= self.data[i][2]:

                val = self.data[i][0]

                if modi(self.dur, i) == InfinityObj:
                    self.inf = True
                    self.inf_value = val

                return val
                   
    def durs(self):

        return self.dur        

    def values(self):

        return [val[0] for val in self.data]


class _infinity:
    """ Used in TimeVars to stay on certain values until re-evaluated """

    def __init__(self):

        pass

    def __str__(self):
        return "<TimeVar.Infinity Object>"

    def __eq__(self, other):

        return other == InfinityObj

    def __ne__(self, other):

        return other != InfinityObj

inf = Inf = _infinity()
