"""
    These are SynthDefs written in Python and sent to Sclang using OSC.

    The reason for doing this is that each one can inherit behaviour from our
    base SynthDef class such that every SynthDef can be manipulated in the
    same way, staying true to Python's duck typing philosophy. It also means that
    one SynthDef, e.g. technobass, could inherit from bass.

"""

from __future__ import division

class SynthDef:
    """ Abstract base class """

    def __init__(self):

        # Default behaviour
        
        self.init = [ ("freq","Line.ar(freq * slidefrom, freq * (1 + slide), sus)"),
                      ("freq","Vibrato.kr(freq, rate: vib, depth: depth, delay:vibDelay, rateVariation: vibVar, depthVariation: depthVar)")]

        self.default = {    "amp"       : 1,
                            "sus"       : 1,
                            "pan"       : 0,
                            "freq"      : 0,
                            "rate"      : 0,
                            "lpf"       : 20000,
                            "hpf"       : 0,
                            "delay"     : 0,
                            "verb"      : 0.25,
                            "echo"      : 0,
                            "echoON"    : 0,
                            "room"      : 0.5,
                            "vib"       : 0,
                            "vibDelay"  : 0,
                            "vibVar"    : 0.04,
                            "depthVar"  : 0.1,
                            "depth"     : 0.02,
                            "slide"     : 0,
                            "slidefrom" : 1 }    

        self.arg =  { "osc"  : [] }
        
        self.env = Env.perc()

    def args(self):
        return ",".join([(str(a[0]) + "=" + str(a[1])) for a in self.default.items()])

    @staticmethod
    def combine(osc1, sign, osc2):
        if type(osc1) is not list:
            osc1 = [osc1]
        if type(osc2) is not list:
            osc2 = [osc2]
        return osc1 + [("osc %s " % sign) + osc for osc in osc2]

    def SynthDef(self, newline=True):
        """ Calculates the SynthDef in SCLang for the class """

        # Start definition

        s = "SynthDef.new( \%s," % self.__class__.__name__
        
        s += "{arg %s;var osc, env;" % self.args()

        # Default frequency modulation

        for key, default in self.init:

            s += "%s = %s;" % (key, default)

        # Add any changes to arguments first

        for arg in [a for a in self.arg.keys() if a != "osc"]:

            if type(self.arg[arg]) is list:

                s += "".join(["%s = %s;" % (str(arg), str(value)) for value in self.arg[arg]])

            else:

                s += "%s = %s;" % (str(arg), str(self.arg[arg]))

        # Get the oscillator

        if type(self.arg["osc"]) is list:

            s +="".join(["osc = %s;" % str(value) for value in self.arg["osc"]])

        else:

            s += "osc = %s;" % str(self.arg["osc"])

        # Apply default filters

        s += "osc = HPF.ar(osc, hpf);"

        s += "osc = LPF.ar(osc, lpf + 1);"

        # Get the envelope

        s += "sus = sus + echo;"
            
        s += "env = %s;" % str(self.env)

        s += "osc = osc * env;"

        # Echo

        #s += "echoON = (echo > 0).asInteger;"

        s += "osc = osc + (echoON * CombN.ar(osc, echo * 0.1, echo * 0.1, (echo * 0.5) * sus, 1));"
        
        # Set the pan and reverb and get it playing!

        s += "Out.ar(0,Pan2.ar( %s, pan));" % "FreeVerb.ar(osc, verb, room)"

        s += "} ).add;"

        if newline:

            s = s.replace(";",";\n")

        return s

class EnvGen:
    """ SuperCollider EnvGen """
    def __init__(self, string):
        self.env = string
    def __call__(self, lvl="amp", sus=(1/2,1/2), curve="\lin"):
        return self.env % ("Env([0,%s,0],[sus * %s, sus * %s], %s)" % (str(lvl), str(sus[0]), str(sus[1]), str(curve)))
    def sclang(self, raw):
        return self.env % ("Env(%s)" % raw)
    def perc(self, atk=0.01, sus="sus", lvl="amp", curve=-4):
        return self.env % ("Env.perc(%s)" % ",".join([str(a) for a in (atk, sus, lvl, curve)]))
    def linen(self, *args):
        return self.env % ("Env.linen(%s)" % ",".join([str(a) for a in args]))
    def sine(self, sus="sus"):
        return self.env % ("Env.sine(%s)" % str(sus))
    def block(self, lvl="amp", sus="sus"):
        return self.env % ("Env([0,%s,%s,0],[0,%s,0])" % (str(lvl), str(lvl), str(sus)))
    def reverse(self, lvl="amp", sus="sus"):
        return self.env % ("Env([0.001,%s,0.01],[%s,0], \exp)" % (str(lvl), str(sus)))

Env = EnvGen("EnvGen.ar(%s.delay(delay), doneAction:2)")

class sample_player(SynthDef):
    """ Used for playing back samples """
    def __init__(self):
        SynthDef.__init__(self)

        # Define new defaults for sample player
        self.init = []
        
        self.default["buf"]   = 0
        self.default["scrub"] = 0
        self.default["grain"] = 0
        self.default["room"]  = 0.1
        self.default["rate"]  = 1

        # Imitates "scratching" of a vinyl record
        
        self.arg["rate"] = "(scrub * LFPar.kr(scrub / 4)) + rate - scrub"

        # Breaks up the sample into smaller chunks

        #self.arg["amp"] = "amp * Blip.ar(2 ** grain, 0, 0.5, 0.5) * 3"
        self.arg["amp"] = "amp * 3"

        # Loads the sample

        self.arg["osc"] = "PlayBuf.ar(1, buf, BufRateScale.ir(buf) * rate) * amp"

        # Set the envelope to account for any effects on the buffer

        self.env = Env.block(sus="sus * 2")

class bass(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["amp"] = "amp*2"
        self.arg["freq"] = "freq/4"
        self.arg["osc"] = "LFTri.ar(freq, mul:amp) + VarSaw.ar(freq, width:0.85, mul: amp) + SinOscFB.ar(freq, mul: amp/2)"

class dirt(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["freq"] = "freq/4"
        self.arg["osc"] = "LFSaw.ar(freq, mul:amp) + VarSaw.ar(freq + 1, width:0.85, mul: amp) + SinOscFB.ar(freq - 1, mul: amp/2)"
        self.env = Env.perc(0.05, "sus", curve=-5)
        
class crunch(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = "LFNoise0.ar(Crackle.kr(1.95) * freq * 15, mul: amp)"
        self.env = Env.perc(0.01,0.1,"amp/2")

class rave(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = "Gendy1.ar(rate-1, mul:amp/2, minfreq:freq, maxfreq:freq*2)"

class pads(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = "SinOsc.ar(freq, mul:amp) + SinOsc.ar(freq + 2, mul:amp)"

class scatter(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = "(Saw.ar( freq , mul:amp / 8) + VarSaw.ar([freq + 2,freq +1], mul:amp/8)) * LFNoise0.ar(rate)"
        self.env = Env.linen(0.01,"sus/2","sus/2")

class banjo(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = "Formant.ar(freq, mul:amp/2) + LFSaw.ar(freq, mul:amp/25)"

class charm(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = ["SinOsc.ar([freq, freq + 2 *2], mul:amp / 4) + VarSaw.ar(freq * 8, 10, mul:amp/8)",
                           "LPF.ar(osc, SinOsc.ar(Line.ar(1,rate*4, sus/8),0,freq*2,freq*2 + 10 ))"]

class bell(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["amp"] = "amp*4"
        self.arg["sus"] = "sus*2.5"
        self.arg["osc"] =  """Klank.ar(`[
                                // frequency ratios
                                [0.501, 1, 0.7,   2.002, 3, 9.6,   2.49, 11, 2.571,  3.05, 6.242, 12.49, 13, 16, 24],
                                // amps
                                [0.002,0.02,0.001, 0.008,0.02,0.004, 0.02,0.04,0.02, 0.005,0.05,0.05, 0.02, 0.03, 0.04],
                                // ring times - "stutter" duplicates each entry threefold
                                [1.2, 0.9, 0.25, 0.14, 0.07].stutter(3)
                                ]
                                , Impulse.ar(0.25), freq, 0, 3)"""

                                #osc = osc * EnvGen.ar(Env([0,1,1,0],[0, 2, 0]), doneAction:2) * amp * 8"""

        self.default["verb"] = 0.5
        self.env = Env.block()

class soprano(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.default["vib"] = 5
        self.default["verb"] = 0.5
        self.arg["amp"] = "amp / 2"
        self.arg["osc"] = ["SinOsc.ar(freq * 3, mul:amp) + SinOscFB.ar(freq * 3, mul:amp / 2)"]
        self.env = Env()

class dub(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["freq"] = "freq / 4"
        self.arg["amp"] = "amp * 2"
        self.arg["osc"] = "LFTri.ar(freq, mul:amp) + SinOscFB.ar(freq,mul: amp)"
        self.env = Env.sine()


class viola(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.init=[]
        self.default["verb"] = 0.33
        self.default["vib"] = 6
        self.arg["osc"] = "PMOsc.ar(freq, Vibrato.kr(freq, rate:vib, depth:0.008, delay: sus * 0.25), 10, mul:amp / 2)"
        self.env = Env.perc("1/4 * sus", "2.5 * sus")
        
##class distort(SynthDef):
##    def __init__(self):
##        SynthDef.__init__(self)
##        pass # TODO

class wiggle(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = "LFSaw.ar(Vibrato.kr(freq,delay:sus/2,rate:6,depth:2,depthVariation:0), mul:amp/16)"
        self.env = Env.sclang("Array.series(15,0,1/15)++[0], Array.fill(14,sus/14)++[0]")

class scratchy(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.default["depth"] = 0.5
        self.default["rate"] = 0.04
        self.arg["freq"] = "freq * Crackle.ar(1.5)"
        self.arg["osc"] = "SinOsc.ar(Vibrato.kr(freq, 2, 3, rateVariation:rate, depthVariation:depth), mul:amp )"

class klank(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["sus"] = "sus * 1.5"
        self.arg["osc"] = "Klank.ar(`[[1,2,3,4], Array.fill(4, 1), Array.fill(4, 2)], {ClipNoise.ar(0.0005)}.dup, freq)"
        self.env = Env()

class sing(klank, soprano):
    """ Combination of klank and soprano """
    def __init__(self):
        klank.__init__(self)
        osc1 = self.arg["osc"]
        soprano.__init__(self)
        osc2 = self.arg["osc"]
        self.arg["osc"] = SynthDef.combine(osc1, "+", osc2)

class pluck(SynthDef):
    """ Credit: Bjorn Westergard """
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["amp"] = "(amp*2) + 0.00001"
        self.arg["freq"] = ["freq","freq + (LFNoise2.ar(50).range(-2,2))"]
        self.arg["osc"] = ["SinOsc.ar(freq * 1.002, phase: VarSaw.ar(freq, width: Line.ar(1,0.2,2))) * 0.3 + SinOsc.ar(freq, phase: VarSaw.ar(freq, width: Line.ar(1,0.2,2))) * 0.3 ",
                           "osc * XLine.ar(amp,(amp)/10000,sus*4) * 0.3"]
        self.env = Env.block(sus="sus*1.5")

class siren(SynthDef):
    """ Credit: Unknown (Thor?) """
    def __init__(self):
        SynthDef.__init__(self)
        self.default["verb"] = 0.33
        self.arg["rate"] = "rate / 10"
        self.arg["freq"] = "LFPulse.kr(rate, 0.99, 0.4).lagud(0.4 / rate, 0.6 / rate) * 800 + freq"
        self.arg["osc"] = [ "LFPulse.ar(freq, 0.99, 0.2).lagud(0.4 / freq, 0.6 / freq) * 2 - 1",
                            "BPF.ar(osc.clip2(0.2), 1500, 1/4) * 4",
                            "osc + DelayC.ar(osc, 0.1, 0.1, 0.3)",
                            "osc * 0.4"]
        
        self.env = Env.block()

class ripple(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["amp"] = "amp/6"
        self.arg["osc"] = ["Pulse.ar([freq/4, freq/4+1],0.2,0.25) + Pulse.ar([freq+2,freq],0.5,0.5)",
                           "osc * SinOsc.ar(rate/ sus,0,0.5,1)"]
        self.env = Env(sus=(0.55,0.55))

class rev(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["amp"] = "amp / 4"
        self.arg["osc"] = "PMOsc.ar(freq, freq * 2 , 10)"
        self.env = Env.reverse()

class sweep(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = ["LFPulse.ar(Crackle.ar(1/4) * freq, 0, Line.ar(0,1,sus*2), 0.2) + VarSaw.ar(Crackle.ar(1/4) * freq + 1 * 2, 2, 2, 0.2, 0.3)",
                           "LPF.ar([osc, osc + Crackle.ar()], XLine.ar(freq / 4, freq * 4, sus / 4) ) / 2",
                           "osc + FreeVerb.ar(osc)"]
        self.env = Env.perc("sus/16","sus*2.5",curve=-10)

class orient(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.default["room"] = 10
        self.default["verb"] = 0.7
        self.arg["osc"] = "LFPulse.ar([freq,freq+1], [0.5,1], [0.25,0.1], 1/4)"

class py(orient):
    def __init__(self):
        orient.__init__(self)
        self.arg["osc"] = "LFCub.ar([freq,freq+1], [0.5,1], [0.25,0.1]) * 2"

class zap(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.default["room"]=0
        self.default["verb"]=0
        self.arg["amp"] = "amp / 10"
        self.arg["osc"] = "Saw.ar( freq * [1,1.01] + LFNoise2.ar(50).range(-2,2) ) + VarSaw.ar( freq + LFNoise2.ar(50).range(-2,2), 1 ) "
        self.env = Env.perc(atk=0.025, curve=-10)
        
class marimba(SynthDef):
    def __init__(self):
        SynthDef.__init__(self)
        self.arg["osc"] = "Klank.ar(`[[1/2, 1, 4, 9], [1/2,1,1,1], [1,1,1,  1]], PinkNoise.ar([0.007, 0.007]), [freq, freq], [0,2])"
        self.arg["sus"] = "sus * 1.5"
        self.env = Env.perc(atk=0.001, curve=-6)
