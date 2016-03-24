"""
    Effects.py

    Module for handling any dynamically added effects to SynthDef nodes

"""

class Handler:

    def __init__(self):

        self.data = {}

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def __iter__(self):

        for item in self.data:

            yield item

    def __getitem__(self, key):

        return self.data[key]

    def __setitem__(self, key, value):

        self.data[key] = value

    def clear(self):
        """ Empties the dictionary """

        while len(self.data) > 0:

            del self.data[self.data.keys()[0]]

        return

    def add(self, name, **kwargs):
        """ Add an effect SynthDef """

        self.data[name] = kwargs

        return
