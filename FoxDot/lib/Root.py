from Patterns.utils import modi
import TimeVar

CHROMATIC_NOTES = ["C"," ","D"," ","E","F"," ","G"," ","A"," ","B"]

class Note:

    def __init__(self, index):

        self.char = None
        self.num  = None

        self.set(index)

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return str(self.num)

    def __float__(self):
        return float(self.num)

    def __int__(self):
        return int(self.num)

    def set(self, index):

        if type(index) is str:

            char = index.title()

            if len(char) == 1:
                mod = 0
            elif len(char) == 2 and char[1] == "#":
                mod = 1
            elif len(char) == 2 and char[1] == "b":
                mod = -1
            else:
                raise TypeError("Could not convert string '%s' to Note" % index)

            self.char = char
            self.num  = (CHROMATIC_NOTES.index(char[0]) + mod) % len(CHROMATIC_NOTES)

        if type(index) is int:

            self.num  = index
            self.char = modi(CHROMATIC_NOTES, index)

        if type(index) is float:

            self.num = index
            self.char = "<Micro-Tuned>"

        if isinstance(index, TimeVar.var):

            self.num = index
            self.char = "<Time-Varying>"

    def __iadd__(self, other):
        self.num += other

    def __isub__(self, other):
        self.num -= other

    def __add__(self, other):
        return self.num + other

    def __sub__(self, other):
        return self.num - other

    def __radd__(self, other):
        return other + self.num

    def __rsub__(self, other):
        return other - self.num

    def __call__(self, *args):

        if len(args) > 0:

            self.set(args[0])

        return self

class __root__:
    def __init__(self):
        self.default = Note("C")
    def __setattr__(self, key, value):
        if key == "default" and key in vars(self):
            self.default.set(value)
        else:
            self.__dict__[key] = value
        return

Root = __root__()
