from Settings import EFFECTS_DIR, SC3_PLUGINS
from ServerManager import Server

class Effect:
    server=Server
    def __init__(self, foxdot_name, synthdef, args=[]):

        self.name      = foxdot_name
        self.synthdef  = synthdef
        self.filename  = EFFECTS_DIR + "/{}.scd".format(self.synthdef)
        self.args      = args
        self.effects   = []
        
    def __repr__(self):
        return "<Fx '{}' -- args: {}>".format(self.synthdef, ",".join(self.args))

    def add(self, string):
        self.effects.append(string)
        return

    def list_effects(self):
        s = ""
        for p in self.effects:
            s += p + ";\n"
        return s
        
    def __str__(self):
        s  = "SynthDef.new(\{},\n".format(self.synthdef)
	s += "{" + "|bus, {}|\n".format(", ".join(self.args))
        s += "var osc;\n"
        s += "osc = In.ar(bus, 2);\n"
        s += self.list_effects()
        s += "ReplaceOut.ar(bus, osc)}).add;"
        return s

    def save(self):
        ''' writes to file and sends to server '''
        with open(self.filename, 'w') as f:
            f.write(self.__str__())
        if self.server is not None:
            self.server.loadSynthDef(self.filename)
        return

class PreEffect(Effect):
    """ SynthDef that modulates argumentes such as frequency
        *before* being used in a UGen. """
    def __init__(self, *args, **kwargs):
        Effect.__init__(self, *args, **kwargs)

class Out(Effect):
    def __init__(self):
        Effect.__init__(self, 'makeSound', 'makeSound')
        self.save()
    def __str__(self):
        s  = "SynthDef.new(\makeSound,\n"
	s += "{ arg bus, sus; var osc;\n"
	s += "	osc = In.ar(bus, 2);\n"
	s += "	Line.ar(dur: sus, doneAction: 14);\n"
	s += "	DetectSilence.ar(osc, amp:0.0001, time: 0.1, doneAction: 14);\n"
	s += "	Out.ar(0, osc)}).add;\n"
	return s

class EffectManager(dict):
    def __init__(self):

        dict.__init__(self)
        self.pre_kw=[]
        self.kw=[]

    def new(self, foxdot_arg_name, synthdef, args, order=2):
        self[foxdot_arg_name] = Effect(foxdot_arg_name, synthdef, args)
        self.kw.append(foxdot_arg_name)
        return self[foxdot_arg_name]
    
    def kwargs(self):
        return tuple(self.pre_kw) + tuple(self.kw)

    def __iter__(self):
        for key in self.pre_kw + self.kw:
            yield key, self[key]


# -- TODO

# Have ordered effects e.g.
# 0. Process frequency / playback rate
# 1. Before envelope
# 2. After envelope


FxList = EffectManager()

# Frequency Effects

##fx = FxList.new("vibrato", "vibrato", ["vibrato", "freq"], order=0)
##fx.add("osc = Vibrato.ar()")
##fx.save()

# Sound effects

fx = FxList.new('hpf','highPassFilter',['hpf', 'resonance'], order=2)
fx.add('osc = RHPF.ar(osc, hpf, resonance)')
fx.save()

fx = FxList.new('lpf','lowPassFilter',['lpf', 'resonance'], order=2)
fx.add('osc = RLPF.ar(osc, lpf, resonance)')
fx.save()

if SC3_PLUGINS:

    fx = FxList.new('bits', 'bitcrush', ['bits', 'sus', 'amp'], order=1)
    fx.add("osc = Decimator.ar(osc, rate: 44100, bits: bits)")
    fx.add("osc = osc * Line.ar(amp * 0.85, 0.0001, sus * 2)") 
    fx.save()

##    fx = FxList.new('grate', 'disintergator', ['grate'])
##    fx.add("osc = Disintegrator.ar(osc, multiplier: grate)")
##    fx.save()

##    fx = FxList.new("distort", "dirtortion", ["distort"])
##    fx.add("osc = CrossoverDistortion.ar(osc, amp: distort)")
##    fx.save()

fx = FxList.new('chop', 'chop', ['chop', 'sus'], order=2)
fx.add("osc = osc * LFPulse.ar(chop / sus, add: 0.1)")
fx.save()

fx = FxList.new('echo', 'combDelay', ['echo', 'sus', 'decay'], order=2)
fx.add('osc = osc + CombL.ar(osc, delaytime: echo * sus, maxdelaytime: 2, decaytime: decay)')
fx.save()

fx = FxList.new('spin', 'spinPan', ['spin','sus'], order=2)
fx.add('osc = osc * [FSinOsc.ar(spin / 2, iphase: 1, mul: 0.5, add: 0.5), FSinOsc.ar(spin / 2, iphase: 3, mul: 0.5, add: 0.5)]')
fx.save()

fx = FxList.new("cut", "trimLength", ["cut", "sus"], order=2)
fx.add("osc = osc * EnvGen.ar(Env(levels: [1,1,0.01], curve: 'step', times: [sus * cut, 0.01]))")
fx.save()

fx = FxList.new('verb', 'reverb', ['verb', 'room'], order=2)
fx.add("osc = FreeVerb.ar(osc, verb, room)")
fx.save()

Out()

    
