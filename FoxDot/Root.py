from Patterns.Operations import modi

CHROMATIC_NOTES = ["C"," ","D"," ","E","F"," ","G"," ","A"," ","B"]

class Note:

    def __init__(self, index):

        self.char = None
        self.num  = None

        self.change(index)

    def change(self, index):

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

            self.change(args[0])

        return self

default = Note("C")
