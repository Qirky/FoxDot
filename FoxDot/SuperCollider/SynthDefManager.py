import SynthDef
from types import ClassType

class SynthDefManager:
    def __init__(self, server):

        self.server = server

        self.synthdefs = []

    def __str__(self):

        return str(self.synthdefs)

    def __repr__(self):

        return repr(self.synthdefs)
        
    def load(self):
        
        reload(SynthDef)

        self.synthdefs = []
        
        for name, cls in vars(SynthDef).items():

            if type(cls) == ClassType:

                if issubclass(cls, SynthDef.SynthDef) and cls != SynthDef.SynthDef:

                    self.synthdefs.append(cls.__name__)
                    
                    self.server.sendsclang(cls().SynthDef(newline=False))

        return

    def names(self):
        for s in self.synthdefs:
            print s
        return self.synthdefs
