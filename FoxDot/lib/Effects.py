"""
    Filter Effects
    --------------

    Effects are added to Player objects as keywords instructions like `dur`
    or `amp` but are a little more tricky. Each effect has a "title" keyword,
    which requires a nonzero value to add the effect to a Player. Effects
    also have other attribute keywords which can be any value and may have
    a default value which is set when a Player is created.

    ::
        # Example. Reverb effect "title" is `room` and attribute is `mix`, which
        # defaults to 0.25. The following adds a reverb effect
        
        p1 >> pads(room=0.5)

        # This still adds the effect, but a mix of 0 doesn't actually do anything

        p1 >> pads(room=0.5, mix=0)

        # This effect is not added as the "title" keyword, room, is 0

        p1 >> pads(room=0, mix=0.5)

    Other effects are outlined below:
    
    *High Pass Filter* - Title keyword: `hpf`, Attribute keyword(s): `hpr`
    Only frequences **above** the value of `hpf` are kept in the final signal. Use `hpr` to set the resonance (usually a value between 0 and 1)

    *Low Pass Filter* - Title keyword: `lpf`, Attribute keyword(s): `lpr`
    Only frequences **below** the value of `lpf` are kept in final signal. Use `lpr` to set the resonance (usually a value between 0 and 1)

    *Bitcrush* - Title keyword: `bits`, Attribute keyword(s): `crush`
    The bit depth, in number of `bits`, that the signal is reduced to; this is a value between 1 and 24 where other values are ignored. Use `crush` to set the amount of reduction to the bitrate (defaults to 8)

    *Reverb* - Title keyword: `room`, Attribute keyword(s): `mix`
    The `room` argument specifies the size of the room and `mix` is the dry/wet mix of reverb; this should be a value between 0 and 1 (defalts to 0.25)

    *Chop* - Title keyword: `chop`, Attribute keyword(s): `sus`
    'Chops' the signal into chunks using a low frequency pulse wave over the sustain of a note.

    *Slide To* - Title keyword: `slide`, Attribute keyword(s):
    Slides' the frequency value of a signal to `freq * (slide+1)` over the  duration of a note (defaults to 0)

    *Slide From* - Title keyword: `slidefrom`, Attribute keyword(s):
    Slides' the frequency value of a signal from `freq * (slidefrom)` over the  duration of a note (defaults to 1)

    *Comb delay (echo)* - Title keyword: `echo`, Attribute keyword(s): `decay`
    Sets the decay time for any echo effect in beats, works best on Sample Player (defaults to 0)

    *Panning* - Title keyword: `pan`, Attribute keyword(s):
    Panning, where -1 is far left, 1 is far right (defaults to 0)

    *Vibrato* - Title keyword: `vib`, Attribute keyword(s): 
    Vibrato (defaults to 0)

    Undocumented: Spin, Shape, Formant, BandPassFilter, Echo


"""

from __future__ import absolute_import, division, print_function

import os.path
from .Settings import EFFECTS_DIR, SC3_PLUGINS
from .ServerManager import DefaultServer

class Effect:
    server=DefaultServer
    def __init__(self, foxdot_name, synthdef, args={}, control=False):

        self.name      = foxdot_name
        self.synthdef  = synthdef
        self.filename  = EFFECTS_DIR + "/{}.scd".format(self.synthdef)
        self.args      = args.keys()
        self.vars      = ["osc"]
        self.defaults  = args
        self.effects   = []
        self.control   = control

        self.suffix    = "kr" if self.control else "ar"
        self.channels  = 1 if self.control else 2

        self.input     = "osc = In.{}(bus, {});\n".format(self.suffix, self.channels)
        self.output    = "ReplaceOut.{}".format(self.suffix)
        
    @classmethod
    def set_server(cls, server):
        cls.server = server
    
    def __repr__(self):
        return "<Fx '{}' -- args: {}>".format(self.synthdef, ", ".join(self.args))

    def __str__(self):
        s  = "SynthDef.new(\{},\n".format(self.synthdef)
        s += "{" + "|bus, {}|\n".format(", ".join(self.args))
        s += "var {};\n".format(",".join(self.vars))
        s += self.input
        s += self.list_effects()
        s += self.output
        s += "(bus, osc)}).add;"
        return s

    def add(self, string):
        self.effects.append(string)
        return

    def doc(self, string):
        """ Set a docstring for the effects"""
        return 

    def list_effects(self):
        s = ""
        for p in self.effects:
            s += p + ";\n"
        return s

    def add_var(self, name):
        if name not in self.vars:
            self.vars.append(name)
        return

    def save(self):
        ''' writes to file and sends to server '''
        
        # 1. See if the file exists

        if os.path.isfile(self.filename):

            with open(self.filename) as f:

                contents = f.read()

        else:

            contents = ""

        # 2. If it does, check contents

        this_string = self.__str__()

        if contents != this_string:

            try:

                with open(self.filename, 'w') as f:
                
                    f.write(this_string)

            except IOError:

                print("IOError: Unable to update '{}' effect.".format(self.synthdef))

        # 3. Send to server
        
        if self.server is not None:

            self.server.loadSynthDef(self.filename)

        return

class In(Effect):
    def __init__(self):
        Effect.__init__(self, 'startSound', 'startSound')
        self.save()      
    def __str__(self):
        s  = "SynthDef.new(\startSound,\n"
        s += "{ arg bus, rate=1, sus; var osc;\n"
        s += "	ReplaceOut.kr(bus, rate)}).add;\n"
        return s

class Out(Effect):
    def __init__(self):
        self.max_duration = 8
        Effect.__init__(self, 'makeSound', 'makeSound')
        self.save()
    def __str__(self):
        s  = "SynthDef.new(\makeSound,\n"
        s += "{ arg bus, sus; var osc;\n"
        s += "	osc = In.ar(bus, 2);\n"
        s += "  osc = EnvGen.ar(Env([1,1,0],[sus * {}, 0.1]), doneAction: 14) * osc;\n".format(self.max_duration)
        s += "	DetectSilence.ar(osc, amp:0.0001, time: 0.1, doneAction: 14);\n"
        #s += "	Out.ar(0, osc);\n"
        s += "Out.ar(0, osc[0]);\n"
        s += "Out.ar(1, osc[1]);\n"
        s += " }).add;\n"
        return s

class EffectManager(dict):
    def __init__(self):

        dict.__init__(self)
        self.kw=[]
        self.all_kw=[]
        self.defaults={}
        self.order={N:[] for N in range(3)}

    def __repr__(self):
        return "\n".join([repr(value) for value in self.values()])

    def new(self, foxdot_arg_name, synthdef, args, order=2):
        self[foxdot_arg_name] = Effect(foxdot_arg_name, synthdef, args, order==0)

        if order in self.order:

            self.order[order].append(foxdot_arg_name)

        else:

            self.order[order] = [foxdot_arg_name]

        # Store the main keywords together

        self.kw.append(foxdot_arg_name)

        # Store other sub-keys

        for arg in args:
            if arg not in self.all_kw:
                self.all_kw.append(arg)

            # Store the default value
            
            self.defaults[arg] = args[arg]

        return self[foxdot_arg_name]
    
    def kwargs(self):
        """ Returns the title keywords for each effect """
        return tuple(self.kw)

    def all_kwargs(self):
        """ Returns *all* keywords for all effects """
        return tuple(self.all_kw)

    def __iter__(self):
        for key in self.pre_kw + self.kw:
            yield key, self[key]


# -- TODO

# Have ordered effects e.g.
# 0. Process frequency / playback rate
# 1. Before envelope
# 2. Adding the envelope
# 3. After envelope

FxList = EffectManager()

# Frequency Effects

fx = FxList.new("vib", "vibrato", {"vib": 0, "vibdepth": 0.02}, order=0)
fx.add("osc = Vibrato.ar(osc, vib, depth: vibdepth)")
fx.save()

fx = FxList.new("slide", "slideTo", {"slide":0, "sus":1, "slidedelay": 0}, order = 0)
fx.add("osc = osc * EnvGen.ar(Env([1, 1, slide + 1], [sus*slidedelay, sus*(1-slidedelay)]))")
fx.save()

fx = FxList.new("slidefrom", "slideFrom", {"slidefrom": 0, "sus": 1, "slidedelay": 0}, order=0)
fx.add("osc = osc * EnvGen.ar(Env([slidefrom + 1, slidefrom + 1, 1], [sus*slidedelay, sus*(1-slidedelay)]))")
fx.save()

fx = FxList.new("bend", "pitchBend", {"bend": 0, "sus": 1, "benddelay": 0}, order=0)
fx.add("osc = osc * EnvGen.ar(Env([1, 1, 1 + bend, 1], [sus * benddelay, (sus*(1-benddelay)/2), (sus*(1-benddelay)/2)]))")
fx.save()

fx = FxList.new("coarse", "coarse", {"coarse": 0, "sus": 1}, order=0)
fx.add("osc = osc * LFPulse.ar(coarse / sus)")
fx.save()

fx = FxList.new("striate", "striate", {"striate": 0, "sus": 1, "buf": 0, "rate": 1}, order=0)
fx.add("osc = osc * LFPulse.ar(striate / sus, width:  (BufDur.kr(buf) / rate) / sus)")
fx.save()

fx = FxList.new("pshift", "pitchShift", {"pshift":0}, order=0)
fx.add("osc = osc * (1.059463**pshift)")
fx.save()

fx = FxList.new("fm_sin", "FrequencyModulationSine", {"fm_sin":0, "fm_sin_i":1}, order=0)
fx.add("osc = osc + (fm_sin_i * SinOsc.kr(osc * fm_sin))")
fx.save()

fx = FxList.new("fm_saw", "FrequencyModulationSaw", {"fm_saw":0, "fm_saw_i":1}, order=0)
fx.add("osc = osc + (fm_saw_i * Saw.kr(osc * fm_saw))")
fx.save()

fx = FxList.new("fm_pulse", "FrequencyModulationPulse", {"fm_pulse":0, "fm_pulse_i":1}, order=0)
fx.add("osc = osc + (fm_pulse_i * Pulse.kr(osc * fm_pulse))")
fx.save()

# Signal effects

fx = FxList.new('hpf','highPassFilter', {'hpf': 0, 'hpr': 1}, order=2)
fx.doc("Highpass filter")
fx.add('osc = RHPF.ar(osc, hpf, hpr)')
fx.save()

fx = FxList.new('lpf','lowPassFilter', {'lpf': 0, 'lpr': 1}, order=2)
fx.add('osc = RLPF.ar(osc, lpf, lpr)')
fx.save()

fx = FxList.new('swell','filterSwell', {'swell': 0, 'sus': 1, 'hpr': 1}, order=2)
fx.add_var("env")
fx.add("env = EnvGen.kr(Env([0,1,0], times:[(sus*0.125), (sus*0.25)], curve:4))")
fx.add('osc = RHPF.ar(osc, env * swell, hpr)')
fx.save()

fx = FxList.new("bpf", "bandPassFilter", {"bpf": 0, "bpr": 1, "bpnoise": 0, "sus": 1}, order=2)
fx.add("bpnoise = bpnoise / sus")
fx.add("bpf = LFNoise1.kr(bpnoise).exprange(bpf * 0.5, bpf * 2)")
fx.add("bpr = LFNoise1.kr(bpnoise).exprange(bpr * 0.5, bpr * 2)")
fx.add("osc = BPF.ar(osc, bpf, bpr)")
fx.save()
       
if SC3_PLUGINS:

    fx = FxList.new('crush', 'bitcrush', {'bits': 8, 'sus': 1, 'amp': 1, 'crush': 0}, order=1)
    fx.add("osc = Decimator.ar(osc, rate: 44100/crush, bits: bits)")
    fx.add("osc = osc * Line.ar(amp * 0.85, 0.0001, sus * 2)") 
    fx.save()

    fx = FxList.new('dist', 'distortion', {'dist': 0, 'tmp': 0}, order=1)
    fx.add("tmp = osc")
    fx.add("osc = CrossoverDistortion.ar(osc, amp:0.2, smooth:0.01)")
    fx.add("osc = osc + (0.1 * dist * DynKlank.ar(`[[60,61,240,3000 + SinOsc.ar(62,mul:100)],nil,[0.1, 0.1, 0.05, 0.01]], osc))")
    fx.add("osc = (osc.cubed * 8).softclip * 0.5")
    fx.add("osc = SelectX.ar(dist, [tmp, osc])")
    fx.save()

# Envelope -- just include in the SynthDef and use asdr?

# Post envelope effects    

fx = FxList.new('chop', 'chop', {'chop': 0, 'sus': 1}, order=2)
fx.add("osc = osc * LFPulse.kr(chop / sus, add: 0.01)")
fx.save()

fx = FxList.new('tremolo', 'tremolo', {'tremolo': 0, 'beat_dur': 1}, order=2)
fx.add("osc = osc * SinOsc.ar( tremolo / beat_dur, mul:0.5, add:0.5)")
fx.save()

fx = FxList.new('echo', 'combDelay', {'echo': 0, 'beat_dur': 1, 'decay': 1}, order=2)
fx.add('osc = osc + CombL.ar(osc, delaytime: echo * beat_dur, maxdelaytime: 2, decaytime: decay * beat_dur)')
fx.save()

fx = FxList.new('spin', 'spinPan', {'spin': 0,'sus': 1}, order=2)
fx.add('osc = osc * [FSinOsc.ar(spin / 2, iphase: 1, mul: 0.5, add: 0.5), FSinOsc.ar(spin / 2, iphase: 3, mul: 0.5, add: 0.5)]')
fx.save()

fx = FxList.new("cut", "trimLength", {"cut": 0, "sus": 1}, order=2)
fx.add("osc = osc * EnvGen.ar(Env(levels: [1,1,0.01], curve: 'step', times: [sus * cut, 0.01]))")
fx.save()

fx = FxList.new('room', 'reverb', {'room': 0, 'mix': 0.1}, order=2)
fx.add("osc = FreeVerb.ar(osc, mix, room)")
fx.save()

fx = FxList.new("formant", "formantFilter", {"formant": 0}, order=2)
fx.add("formant = (formant % 8) + 1")
fx.add("osc = Formlet.ar(osc, formant * 200, ((formant % 5 + 1)) / 1000, (formant * 1.5) / 600).tanh")
fx.save()

fx = FxList.new("shape", "wavesShapeDistortion", {"shape":0}, order=2)
fx.add("osc = (osc * (shape * 50)).fold2(1).distort / 5")
fx.save()

In(); Out()
Effect.server.setFx(FxList)
