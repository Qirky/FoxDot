"""
    SCLang.py
"""

from ..ServerManager  import SCLangManager
from copy import copy

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
Pan2     = cls("Pan2")
LPF      = cls("LPF")
BPF      = cls("BPF")
HPF      = cls("HPF")
DelayC   = cls("DelayC")
CombN    = cls("CombN")
Crackle  = cls("Crackle")

ClipNoise    = cls("ClipNoise")
BufRateScale = cls("BufRateScale")

# Default Arguments
    
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

osc = instance("osc")
env = instance("env")


"""
    Envelope Generator
    ==================
"""

class EnvGen(instance):

    shortarg = { 'attackTime'  : 'atk',
                 'releaseTime' : 'sus',
                 'level'       : 'lvl' }
    
    defaults = { 'releaseTime' : sus,
                 'level' : amp }
    
    def __init__(self, string):
        self.value = str(string)
    def __call__(self, *args, **kwargs):
        if not self.ismethod():
            kwargs['levels'] = args[0] if args else kwargs.get('levels', [0,amp,0])
            kwargs['times']  = args[1] if args else kwargs.get('times', [sus / 2,sus / 2])
        return instance.__call__(self, *args, **kwargs)
    def ismethod(self):
        return '.' in self.value
    def __str__(self):
        return str( cls("EnvGen").ar(instance(self.value).delay(delay), doneAction=2))
    def block(self, *args, **kwargs):
        return self.__call__([0,amp,amp,0],[0,kwargs.get("sus",sus),0])
        
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

    server = SCLangManager()
    var = ['osc', 'env']

    def __init__(self, name):
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
                            "room"      : 0.5,
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
                
        self.name = name
        self.osc = osc
        self.env = env
        self.base()

    def base(self):
        # Base-class behaviour
        self.freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus)
        self.freq = Vibrato.kr(self.freq, rate=vib, depth=depth, delay=vibDelay, rateVariation=vibVar, depthVariation=depthVar)
        self.env  = Env.perc()
        return

    def __getattr__(self, key):
        if key in self.defaults:
            return instance(key)
        else:
            raise AttributeError("Attribute '{}' not found".format(key))
    
    def add(self):
        self.osc = HPF.ar(self.osc, hpf)
        self.osc = LPF.ar(self.osc, lpf + 1)
        try:
            SynthDef.server.sendsclang(str(self))
            SynthDefs[self.name] = str(self)
        except:
            print "SynthDef '{}' could not be added to the server".format(self.name)

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

    @staticmethod
    def echo_effect():
        return echoOn * CombN.ar(osc, echo * 0.1, echo * 0.1, (echo * 0.5) * sus, 1)

    def __str__(self):
        name     = str(self.name)
        defaults = str(format_args(kwargs=self.defaults, delim='='))
        mod      = str(self.modify())
        snd      = osc + SynthDef.echo_effect()
        sound    = str(Out.ar(0, Pan2.ar(FreeVerb.ar(snd * env, verb, room), pan)))
        return "SynthDef.new( \%s,{|%s|%s%s}).add;" % (name, defaults, mod, sound)

    def __repr__(self):
        return str(self.name)

    def __add__(self, other):
        if not isinstance(other, SynthDef):
            raise TypeError("Warning: '{}' is not a SynthDef".format(str(other)))
        new = copy(self)
        new.osc = self.osc + other.osc
        return new

# Array manipulation emulator functions

stutter = lambda array, n: [item for item in array for i in range(n)]
dup = lambda x: [x, x]
        
