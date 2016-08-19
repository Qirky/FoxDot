"""
    SCLang.py
"""

from ..ServerManager import Server
from copy import copy
import StringIO
import os

def format_args(args=[], kwargs={}, delim=': '):
    return ", ".join([str(a) for a in args] + ["%s%s%s" % (key, delim, value) for key, value in kwargs.items()])

class cls:
    def __init__(self, name, **kwargs):
        self.name = name
        self.ref  = kwargs.get("ref", "")
    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self.name)
    def __call__(self):
        return instance("{}({}{})".format(self.name, self.ref, format_args(args, kwargs)))
    def ar(self, *args, **kwargs):
        return instance("{}.ar({}{})".format(self.name, self.ref, format_args(args, kwargs)))
    def kr(self, *args, **kwargs):
        return instance("{}.kr({}{})".format(self.name, self.ref, format_args(args, kwargs)))
    def ir(self, *args, **kwargs):
        return instance("{}.ir({}{})".format(self.name, self.ref, format_args(args, kwargs)))

class instance:
    defaults = {}
    shortarg = {}
    def __init__(self, string):
        self.value = str(string)
    def __repr__(self):
        return str(self.value)
    def __str__(self):
        return str(self.value)    
    def __add__(self, other):
        return instance("(%s)" % (str(self) + " + " + str(other)))
    def __sub__(self, other):
        return instance("(%s)" % (str(self) + " - " + str(other)))
    def __mul__(self, other):
        return instance("(%s)" % (str(self) + " * " + str(other)))
    def __div__(self, other):
        return instance("(%s)" % (str(self) + " / " + str(other)))
    def __pow__(self, other):
        return instance("(%s)" % (str(self) + " ** " + str(other)))
    def __xor__(self, other):
        return instance("(%s)" % (str(self) + " ** " + str(other)))
    def __truediv__(self, other):
        return self.__div__(other)
    def __radd__(self, other):
        return instance("(%s)" % (str(other) + " + " + str(self)))
    def __rsub__(self, other):
        return instance("(%s)" % (str(other) + " - " + str(self)))
    def __rmul__(self, other):
        return instance("(%s)" % (str(other) + " * " + str(self)))
    def __rdiv__(self, other):
        return instance("(%s)" % (str(other) + " / " + str(self)))
    def __rpow__(self, other):
        return instance("(%s)" % (str(other) + " ** " + str(self)))
    def __rxor__(self, other):
        return instance("(%s)" % (str(other) + " ** " + str(self)))
    def __rtruediv__(self, other):
        return self.__rdiv__(other)
    def __mod__(self, other):    
        return instance(str(self.value) % str(other)) if "%" in self.value else self
    def __coerce__(self, other):
        try:
            self = instance(str(self))
            other = instance(str(other))
            return (self, other)
        except:
            return

    def __getattr__(self, name, *args, **kwargs):
        return self.custom('.' + name, *args, **kwargs)

    def string(self):
        return str(self.value) + "{}"

    def custom(self, name):
        return self.__class__(self.string().format(name))
    
    def __call__(self, *args, **kwargs):

        for arg in set(self.defaults.keys() + self.shortarg.keys()):
            
            if arg in self.shortarg:

                if self.shortarg[arg] in kwargs:

                    kwargs[arg] = kwargs.get(self.shortarg[arg], self.default[arg])

                    del kwargs[self.shortarg[arg]]

                    continue

            if arg in self.defaults:

                kwargs[arg] = kwargs.get(arg, self.defaults[arg])
            
        return self.__class__(self.string().format("({})".format(format_args(args, kwargs))))
        

# UGens

SinOsc    = cls("SinOsc")
SinOscFB  = cls("SinOscFB")
Saw       = cls("Saw")
LFSaw     = cls("LFSaw")
VarSaw    = cls("VarSaw")
LFTri     = cls("LFTri")
LFPar     = cls("LFPar")
PlayBuf   = cls("PlayBuf")
LFNoise0  = cls("LFNoise0")
LFNoise1  = cls("LFNoise1")
LFNoise2  = cls("LFNoise2")
Gendy1    = cls("Gendy1")
Gendy2    = cls("Gendy2")
Gendy3    = cls("Gendy3")
Gendy4    = cls("Gendy4")
Gendy5    = cls("Gendy5")
Formant   = cls("Formant")
Pulse     = cls("Pulse")
LFPulse   = cls("LFPulse")
PMOsc     = cls("PMOsc")
Crackle   = cls("Crackle")
LFCub     = cls("LFCub")
PinkNoise = cls("PinkNoise")
Impulse   = cls("Impulse")

# Contain ` references

Klank     = cls("Klank", ref="`")

# Other

Out      = cls("Out")
Vibrato  = cls("Vibrato")
Line     = cls("Line")
XLine    = cls("XLine")
FreeVerb = cls("FreeVerb")
GVerb    = cls("GVerb")
Pan2     = cls("Pan2")
LPF      = cls("LPF")
BPF      = cls("BPF")
HPF      = cls("HPF")
DelayC   = cls("DelayC")
CombN    = cls("CombN")
Crackle  = cls("Crackle")

ClipNoise    = cls("ClipNoise")
BufRateScale = cls("BufRateScale")
BufChannels  = cls("BufChannels")
BufFrames    = cls("BufFrames")

"""
    Envelope Generator
    ==================
"""

class EnvGen(instance):

    shortarg = { 'attackTime'  : 'atk',
                 'releaseTime' : 'sus',
                 'level'       : 'lvl' }

    sus = instance('sus')
    amp = instance('amp')
    
    defaults = { 'releaseTime' : sus,
                 'level'       : amp }
    
    def __init__(self, string):
        self.value = str(string)
    def __call__(self, *args, **kwargs):
        if not self.ismethod():
            kwargs['levels'] = args[0] if args else kwargs.get('levels', [0,self.amp,0])
            kwargs['times']  = args[1] if args else kwargs.get('times', [self.sus / 2] * 2)
        return instance.__call__(self, *args, **kwargs)
    def ismethod(self):
        return '.' in self.value
    def __str__(self):
        return str( cls("EnvGen").ar(instance(self.value).delay(instance('delay')), doneAction=2))
    """ Custom Envelopes """
    def block(self, *args, **kwargs):
        return self.__call__([0,self.amp,self.amp,0],[0,kwargs.get("sus", self.sus),0])
    def reverse(self, *args, **kwargs):
        return self.__call__(levels=[0.001, self.amp, 0.001], times=[kwargs.get("sus", self.sus), 0.001], curve="'exp'")
        
Env = EnvGen("Env")

# Container for SynthDefs

class SynthDict(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
    def __str__(self):
        return str(self.keys())
    def __call__(self, name):
        return self[name]

SynthDefs = SynthDict()

# SynthDef Base Class

class SynthDef:

    server = Server
    var = ['osc', 'env']

    osc = instance("osc")
    env = instance("env")
    
    freq        = instance("freq")
    output      = instance("output")
    sus         = instance("sus")
    amp         = instance("amp")
    pan         = instance("pan")
    rate        = instance("rate")
    lpf         = instance("lpf")
    hpf         = instance("hpf")
    delay       = instance("delay")
    verb        = instance("verb")
    echo        = instance("echo")
    echoOn      = instance("echoOn")
    room        = instance("room")
    vib         = instance("vib")
    vibDelay    = instance("vibDelay")
    vibVar      = instance("vibVar")
    depthVar    = instance("depthVar")
    depth       = instance("depth")
    slide       = instance("slide")
    slidefrom   = instance("slidefrom")
    buf         = instance("buf")
    scrub       = instance("scrub")
    grain       = instance("grain")

    def __init__(self, name):
        self.name = name
        self.filename = os.path.realpath(__file__ + "/../scsyndef/{}.scd".format(self.name))
        
        self.defaults = {   "amp"       : 1,
                            "sus"       : 1,
                            "pan"       : 0,
                            "freq"      : 0,
                            "rate"      : 0,
                            "lpf"       : 20000,
                            "hpf"       : 0,
                            "delay"     : 0,
                            "verb"      : 0.25,
                            "echo"      : 0,
                            "echoOn"    : 0,
                            "room"      : 1,
                            "vib"       : 0,
                            "vibDelay"  : 0,
                            "vibVar"    : 0.04,
                            "depthVar"  : 0.1,
                            "depth"     : 0.02,
                            "slide"     : 0,
                            "slidefrom" : 1 ,
                            "buf"       : 0,
                            "scrub"     : 0,
                            "grain"     : 0 }

        self.base()

    # Context Manager

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.add()

    def base(self):
        # Base-class behaviour
        self.freq = Line.ar(self.freq * self.slidefrom, self.freq * (1 + self.slide), self.sus)
        self.freq = Vibrato.kr(self.freq, rate=self.vib, depth=self.depth, delay=self.vibDelay, rateVariation=self.vibVar, depthVariation=self.depthVar)
        self.env  = Env.perc()
        return

    def __getattr__(self, key):
        if key in self.defaults:
            return instance(key)
        else:
            raise AttributeError("Attribute '{}' not found".format(key))
    
    def add(self):
        """ This is required to add the SynthDef to the SuperCollider Server """

        #  This adds any filters

        self.osc = HPF.ar(self.osc, self.hpf)
        self.osc = LPF.ar(self.osc, self.lpf + 1)
        
        try:
            # Write file
            self.write()

            # Load to server
            SynthDef.server.loadSynthDef(self.filename)

            # Add to list
            SynthDefs[self.name] = self
            
        except:
            
            print "Error: SynthDef '{}' could not be added to the server".format(self.name)
            
        return None

    def write(self):
        """  Writes the SynthDef to file """
        f = open(self.filename, 'w')
        f.write(self.__str__())
        f.close()
        return None
        
    def modify(self):
        string = "var {};\n".format(",".join(self.var)) if self.var else ""
        for arg in self.defaults.keys() + self.var:
            if arg in self.__dict__:
                string = string + str(arg) + '=' + str(self.__dict__[arg]) + ';\n'
        return string

    def rename(self, newname):
        new = copy(self)
        new.name = str(newname)
        return new

    def echo_effect(self):
        return self.echoOn * CombN.ar(self.osc, self.echo * 0.1, self.echo * 0.1, (self.echo * 0.5) * self.sus, 1)

    def __str__(self):
        name     = str(self.name)
        defaults = str(format_args(kwargs=self.defaults, delim='='))
        mod      = str(self.modify())
        snd      = self.osc + self.echo_effect()
        sound    = str(Out.ar(0, Pan2.ar(FreeVerb.ar('osc * env', self.verb, self.room), self.pan)))
        return "SynthDef.new( \%s,{|%s|%s%s}).add;" % (name, defaults, mod, sound)
        #return "SynthDef.new( \%s,{|%s|%s%s})" % (name, defaults, mod, sound)

    def __repr__(self):
        return str(self.name)

    def __add__(self, other):
        if not isinstance(other, SynthDef):
            raise TypeError("Warning: '{}' is not a SynthDef".format(str(other)))
        new = copy(self)
        new.osc = self.osc + other.osc
        return new

    def __call__(self, degree=0, **kwargs):
        return SynthDefProxy(self.name, degree, kwargs)

class SynthDefProxy:
    def __init__(self, name, degree, kwargs):
        self.name = name
        self.degree = degree
        self.mod = 0
        self.kwargs = kwargs
        self.methods = {}
        self.vars = vars(self)
    def __str__(self):
        return "<SynthDef Proxy '{}'>".format(self.name)
    def __add__(self, other):
        self.mod = other
        return self
    def __coerce__(self, other):
        return None
    def __getattr__(self, name):
        if name not in self.vars:
            def func(*args, **kwargs):
                self.methods[name] = (args, kwargs)
                return self
            return func
        else:
            return getattr(self, name)
        

# Array manipulation emulator functions

stutter = lambda array, n: [item for item in array for i in range(n)]
dup = lambda x: [x, x]
        
