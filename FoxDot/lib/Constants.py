from __future__ import absolute_import, division, print_function

class const:
    """ A number value that cannot be changed """
    def __init__(self, value):
        self.value=value
    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)
    def __str__(self):
        return str(self.value)
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
