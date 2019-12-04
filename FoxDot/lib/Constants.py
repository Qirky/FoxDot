from __future__ import absolute_import, division, print_function

from .Patterns import Pattern, PGroup

# Constants and constant values

class const:
    """ A number value that cannot be changed """
    def __init__(self, value):

        if isinstance(value, (list, Pattern)):
            self.__class__ = Pattern
            self.__init__([const(x) for x in value])
        elif isinstance(value, tuple):
            self.__class__ = PGroup
            self.__init__([const(x) for x in value])
        elif isinstance(value, PGroup):
            self.__class__ = value.__class__
            self.__init__([const(x) for x in value])
        else:
            self.value = value

    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)
    def __repr__(self):
        return str(self.value)
    def __add__(self, other):
        return self.value
    def __radd__(self, other):
        return self.value
    def __sub__(self, other):
        return self.value
    def __rsub__(self, other):
        return self.value
    def __mul__(self, other):
        return self.value
    def __rmul__(self, other):
        return self.value
    def __div__(self, other):
        return self.value
    def __rdiv__(self, other):
        return self.value
    def __gt__(self, other):
        return self.value > other
    def __ge__(self, other):
        return  self.value >= other
    def __lt__(self, other):
        return self.value < other
    def __le__(self, other):
        return self.value <= other
    def __eq__(self, other):
        return self.value == other
    def __ne__(self, other):
        return self.value != other

class _inf(const):
    def __repr__(self):
        return "inf"
    def __add__(self, other):
        return _inf(self.value + other)
    def __radd__(self, other):
        return _inf(other + self.value)
    def __sub__(self, other):
        return _inf(self.value - other)
    def __rsub__(self, other):
        return _inf(other - self.value)
    def __mul__(self, other):
        return _inf(self.value * other)
    def __rmul__(self, other):
        return _inf(other * self.value)
    def __div__(self, other):
        return _inf(self.value / other)
    def __rdiv__(self, other):
        return _inf(other / self.value)
    def __truediv__(self, other):
        return _inf(self.value / other)
    def __rtruediv__(self, other):
        return _inf(other / self.value)
    def __eq__(self, other):
        return isinstance(other, _inf)
    def __gt__(self, other):
        return not isinstance(other, _inf)
    def __ge__(self, other):
        return True
    def __lt__(self, other):
        return False
    def __le__(self, other):
        return isinstance(other, _inf)

inf = _inf(0)

class NoneConst(const):
    def __init__(self):
        self.value = None