from __future__ import division

from SCLang import *

# Sample Player

sp = SynthDef("sample_player")
sp.defaults.update(room=0.1 ,rate=1)
sp.rate = scrub * LFPar.kr(scrub / 4) + rate - scrub
sp.osc = PlayBuf.ar(1, buf, BufRateScale.ir(buf) * rate) * amp * 3
sp.env = Env.block(sus=sus*2)
sp.add()

# Synth Players

pads = SynthDef("pads")
pads.osc = SinOsc.ar(freq, mul=amp) +  SinOsc.ar(freq + 2, mul=amp)
pads.env = Env.perc()
pads.add()

bass = SynthDef("bass")
bass.amp = amp * 2
bass.freq = bass.freq / 4
bass.osc = LFTri.ar(freq, mul=amp) + VarSaw.ar(freq, width=0.85, mul=amp) + SinOscFB.ar(freq, mul=amp/2)
bass.env = Env.perc()
bass.add()

dirt = SynthDef("dirt")
dirt.freq = freq / 4
dirt.osc  = LFSaw.ar(freq, mul=amp) + VarSaw.ar(freq + 1, width=0.85, mul=amp) + SinOscFB.ar(freq - 1, mul=amp/2)
dirt.env  = Env.perc()
dirt.add()

crunch = SynthDef("crunch")
crunch.osc = LFNoise0.ar(Crackle.kr(1.95) * freq * 15, mul=amp)
crunch.env = Env.perc(0.01,0.1, amp / 2)
crunch.add()

rave = SynthDef("rave")
rave.osc = Gendy1.ar(rate-1, mul=amp/2, minfreq=freq, maxfreq=freq*2)
rave.env = Env.perc()
rave.add()

scatter = SynthDef("scatter")
scatter.osc = (Saw.ar( freq , mul=amp / 8) + VarSaw.ar([freq + 2,freq +1], mul=amp/8)) * LFNoise0.ar(rate)
scatter.env = Env.linen(0.01, sus/2, sus/2)
scatter.add()

charm = SynthDef("charm")
charm.osc = SinOsc.ar([freq, freq + 2 * 2], mul=amp / 4) + VarSaw.ar(freq * 8, 10, mul=amp/8)
charm.osc = LPF.ar(charm.osc, SinOsc.ar(Line.ar(1,rate*4, sus/8),0,freq*2,freq*2 + 10 ))
charm.env = Env.perc()

bell = SynthDef("bell")
bell.defaults.update(verb = 0.5)
bell.amp = amp * 4
bell.sus = 2.5
bell.osc = Klank.ar([ [0.501, 1, 0.7,   2.002, 3, 9.6,   2.49, 11, 2.571,  3.05, 6.242, 12.49, 13, 16, 24],
                      [0.002,0.02,0.001, 0.008,0.02,0.004, 0.02,0.04,0.02, 0.005,0.05,0.05, 0.02, 0.03, 0.04],
                      stutter([1.2, 0.9, 0.25, 0.14, 0.07], 3) ], Impulse.ar(0.25), freq, 0, 3)
bell.env = Env.block()
bell.add()

soprano = SynthDef("soprano")
soprano.defaults.update(vib=5, verb=0.5)
soprano.amp = amp / 2
soprano.osc = SinOsc.ar(freq * 3, mul=amp) + SinOscFB.ar(freq * 3, mul=amp / 2)
soprano.env = Env()
soprano.add()

dub = SynthDef("dub")
dub.freq = freq / 4
dub.amp = amp * 2
dub.osc = LFTri.ar(freq, mul=amp) + SinOscFB.ar(freq, mul=amp)
dub.env = Env.sine(dur=sus)
dub.add()

viola = SynthDef("viola")
viola.defaults.update(verb=0.33, vib=6)
viola.osc = PMOsc.ar(freq, Vibrato.kr(freq, rate=vib, depth=0.008, delay=sus*0.25), 10, mul=amp / 2)
viola.env = Env.perc( 1/4 * sus, 5/2 * sus )
viola.add()

scratch = SynthDef("scratch")
scratch.defaults.update(depth=0.5, rate=0.04)
scratch.freq = freq * Crackle.ar(1.5)
scratch.osc  = SinOsc.ar(Vibrato.kr(freq, 2, 3, rateVariation=rate, depthVariation=depth), mul=amp )
scratch.env  = Env()
scratch.add()

klank = SynthDef("klank")
klank.sus = sus * 1.5
klank.osc = Klank.ar([[1,2,3,4],[1,1,1,1],[2,2,2,2]], ClipNoise.ar(0.0005).dup, freq)
klank.env = Env()
klank.add()

sing = (soprano + klank).rename("sing")
sing.add()

pluck = SynthDef("pluck")
pluck.amp = amp * 2 + 0.00001
pluck.freq = [freq, freq + LFNoise2.ar(50).range(-2,2)]
pluck.osc = SinOsc.ar(freq * 1.002, phase=VarSaw.ar(freq, width=Line.ar(1,0.2,2))) * 0.3 + SinOsc.ar(freq, phase=VarSaw.ar(freq, width=Line.ar(1,0.2,2))) * 0.3
pluck.osc = pluck.osc * XLine.ar(amp, amp/10000, sus * 4) * 0.3
pluck.env = Env.block(sus=sus*1.5)
pluck.add()

ripple = SynthDef("ripple")
ripple.amp = amp / 6
ripple.osc = Pulse.ar([freq/4, freq/4+1 ],0.2,0.25) + Pulse.ar([freq+2,freq],0.5,0.5)
ripple.osc = ripple.osc * SinOsc.ar(rate/sus,0,0.5,1)
ripple.env = Env(sus=[0.55,0.55])
ripple.add()

rev = SynthDef("rev")
rev.amp = amp / 4
rev.osc = PMOsc.ar(freq, freq * 2, 10)
#rev.env = Env.reverse()
rev.add()

orient = SynthDef("orient")
orient.defaults.update(room=10, verb=0.7)
orient.osc = LFPulse.ar([freq,freq+1], [0.5,1], [0.25,0.1], 1/4)
orient.env = Env.perc()
orient.add()

# Psuedo Inheritance
py = orient.rename("py")
py.osc = LFCub.ar([freq,freq+1], [0.5,1], [0.25,0.1]) * 2
py.add()

zap = SynthDef("zap")
zap.defaults.update(room=0, verb=0)
zap.amp = amp / 10
zap.osc = Saw.ar( freq * [1, 1.01] + LFNoise2.ar(50).range(-2,2) ) + VarSaw.ar( freq + LFNoise2.ar(50).range(-2,2), 1 )
zap.env = Env.perc(atk=0.025, curve=-10)
zap.add()

marimba = SynthDef("marimba")
marimba.osc = Klank.ar([[1/2, 1, 4, 9], [1/2,1,1,1], [1,1,1,1]], PinkNoise.ar([0.007, 0.007]), [freq, freq], [0,2])
marimba.sus = 1
marimba.env = Env.perc(atk=0.001, curve=-6)
marimba.add()
