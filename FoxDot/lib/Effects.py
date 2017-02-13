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
        self.kw=[]
    def new(self, foxdot_arg_name, synthdef, args):
        self[foxdot_arg_name] = Effect(foxdot_arg_name, synthdef, args)
        self.kw.append(foxdot_arg_name)
        return self[foxdot_arg_name]
    def kwargs(self):
        return tuple(self.kw)
    def __iter__(self):
        for key in self.kw:
            yield key, self[key]
    

FxList = EffectManager()

# Order matters

fx = FxList.new('hpf','highPassFilter',['hpf'])
fx.add('osc = HPF.ar(osc, hpf)')
fx.save()

fx = FxList.new('lpf','lowPassFilter',['lpf'])
fx.add('osc = LPF.ar(osc, lpf)')
fx.save()

if SC3_PLUGINS:

    fx = FxList.new('bits', 'bitcrush', ['bits', 'sus', 'amp'])
    fx.add("osc = Decimator.ar(osc, rate: 44100, bits: bits)")
    fx.add("osc = osc * Line.ar(amp * 0.85, 0.0001, sus)") 
    fx.save()

fx = FxList.new('chop', 'chop', ['chop', 'sus'])
fx.add("osc = osc * LFPulse.ar(chop / sus, add: 0.01)")
fx.save()

fx = FxList.new('echo', 'combDelay', ['echo'])
fx.add('osc = osc + CombL.ar(osc, delaytime: echo, maxdelaytime: 2)')
fx.save()

fx = FxList.new('spin', 'spinPan', ['spin','sus'])
fx.add('osc = osc * [FSinOsc.ar(spin / 2, iphase: 1, mul: 0.5, add: 0.5), FSinOsc.ar(spin / 2, iphase: 3, mul: 0.5, add: 0.5)]')
fx.save()

fx = FxList.new('verb', 'reverb', ['verb', 'room'])
fx.add("osc = FreeVerb.ar(osc, verb, room)")
fx.save()

Out()

    
