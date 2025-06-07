from __future__ import absolute_import, division, print_function
import inspect

from ..SCLang.SCLang import *

# To be moved to SCLang later

EnvGen = cls("EnvGen")
Env    = cls("Env")

class _Effect:
    _in = "osc"
    def __init__(self):
        self.lines = []
    def __call__(self, order=0):
        def decorator(effect):
            effect_data = inspect.getfullargspec(effect) # Original args and defaults
            
            # Get filename from function name
            filename = "{}.scd".format(effect.__name__)# filename
            
            # Supplies arg names 
            effect(*map(instance, effect_data.args)) 
            
            # Default values for arguments, to store
            defaults = dict(zip(effect_data.args, effect_data.defaults)) 
        
        return decorator

    def In(self):
        """ Returns 'osc', which is where In.ar() is stored """
        return self._in

    def Out(self, output):
        """ Writes to file and loads synthdef """
        print(";\n".join(self.lines))
        self.lines = []
        return output

    def add(self, *args, **kwargs):
        lines = ["{} = {}".format(key, value) for key, value in kwargs.items()]
        self.lines.extend(lines)
        return

Effect = _Effect() # singleton

@Effect(order=0)
def vibrato(vib=0, vibdepth=0.02):
    osc = Vibrato.ar(Effect.In(), vib, depth=vibdepth)
    return Effect.Out(osc)

@Effect(order=0)
def slideTo(slide=0, sus=1, slide_delay=0):
    osc = Effect.In() * EnvGen.ar(Env([1, 1, slide + 1], [sus * slide_delay, sus * (1 - slide_delay)]))
    return Effect.Out(osc)

@Effect(order=0)
def slideFrom(slide_from=0, sus=1, slide_delay=0):
    osc = Effect.In() * EnvGen.ar(Env([slide_from + 1, slide_from + 1, 1], [sus * slide_delay, sus * (1 - slide_delay)]))
    return Effect.Out(osc)

# fx = FxList.new("glide", "glissando", {"glide": 0, "glide_delay": 0.5, "sus": 1}, order=0)
# fx.add("osc = osc * EnvGen.ar(Env([1, 1, (1.059463**glide)], [sus*glide_delay, sus*(1-glide_delay)]))")
# fx.save()

# fx = FxList.new("bend", "pitchBend", {"bend": 0, "sus": 1, "benddelay": 0}, order=0)
# fx.add("osc = osc * EnvGen.ar(Env([1, 1, 1 + bend, 1], [sus * benddelay, (sus*(1-benddelay)/2), (sus*(1-benddelay)/2)]))")
# fx.save()

# fx = FxList.new("coarse", "coarse", {"coarse": 0, "sus": 1}, order=0)
# fx.add("osc = osc * LFPulse.ar(coarse / sus)")
# fx.save()

# fx = FxList.new("striate", "striate", {"striate": 0, "sus": 1, "buf": 0, "rate": 1}, order=0)
# fx.add("osc = osc * LFPulse.ar(striate / sus, width:  (BufDur.kr(buf) / rate) / sus)")
# fx.save()

# fx = FxList.new("pshift", "pitchShift", {"pshift":0}, order=0)
# fx.add("osc = osc * (1.059463**pshift)")
# fx.save()

@Effect(order=2)
def formantFilter(formant=0):
    Effect.add(formant = (formant % 8) + 1)
    Effect.add(osc = Formlet.ar(Effect.In(), formant * 200, (formant % 5 + 1) / 1000, (formant * 1.5) / 600).tanh)
    Effect.Out() 

@Effect(order=2)
def filterSwell(swell=0, sus=1, hpr=1):
    env = EnvGen.kr(Env([0, 1, 0], times = [(sus * 0.25), (sus * 0.25)], curve="\\sin"))
    osc = RHPF.ar(Effect.In(), env * swell * 2000, hpr)
    return Effect.Out(osc)

