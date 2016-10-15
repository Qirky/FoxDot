import Base

class PComparison:
    def __init__(self, func):
        self.func = func
    def __call__(self, a, b):
        # 'a' will always be a pattern 
        if isinstance(b, Base.metaPattern):
            # If both 'a' and 'b' are being accessed
            if a._now != None and b._now != None:
                a = a._now
                b = b._now
            else:
                a = a.data
                b = b.data

        # If b is a list, just compare to the whole of a
        elif isinstance(b, list):
            a = a.data
        else:
            a = a._now
        return self.func(a, b)
    

Peq = PComparison(lambda a, b: a == b)
Pne = PComparison(lambda a, b: a != b)
Pgt = PComparison(lambda a, b: a > b)
Pge = PComparison(lambda a, b: a >= b)
Plt = PComparison(lambda a, b: a < b)
Ple = PComparison(lambda a, b: a <= b)
