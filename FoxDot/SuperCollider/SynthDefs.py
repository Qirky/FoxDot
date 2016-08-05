from __future__ import division
from SCLang import *

# Sample Player

with SynthDef("sample_player") as sd:
    sd.defaults.update(room=0.1 ,rate=1)
    sd.rate = sd.scrub * LFPar.kr(sd.scrub / 4) + sd.rate - sd.scrub
    sd.osc  = PlayBuf.ar(1, sd.buf, BufRateScale.ir(sd.buf) * sd.rate, trigger=LFPar.kr(sd.grain), startPos=Line.kr(0,BufFrames.kr(sd.buf)*0.75,sd.sus*2)) * sd.amp * 3
    sd.env  = Env.block(sus=sd.sus*2)

# Synth Players

with SynthDef("pads") as p:
    p.osc = SinOsc.ar(p.freq, mul=p.amp) +  SinOsc.ar(p.freq + 2, mul=p.amp)
    p.env = Env.perc()

with SynthDef("bass") as sd:
    sd.amp  = sd.amp * 2
    sd.freq = sd.freq / 2
    sd.osc  = LFTri.ar(sd.freq, mul=sd.amp) + VarSaw.ar(sd.freq, width=0.85, mul=sd.amp) + SinOscFB.ar(sd.freq, mul=sd.amp/2)
    sd.env  = Env.perc()

with SynthDef("dirt") as sd:
    sd.amp  = sd.amp * 0.8
    sd.freq = sd.freq / 2
    sd.osc  = LFSaw.ar(sd.freq, mul=sd.amp) + VarSaw.ar(sd.freq + 1, width=0.85, mul=sd.amp) + SinOscFB.ar(sd.freq - 1, mul=sd.amp/2)
    sd.env  = Env.perc()

with SynthDef("crunch") as sd:
    sd.amp = sd.amp * 0.5
    sd.osc = LFNoise0.ar(Crackle.kr(1.95) * sd.freq * 15, mul=sd.amp)
    sd.env = Env.perc(0.01,0.1, sd.amp / 4)

with SynthDef("rave") as sd:
    sd.osc = Gendy1.ar(sd.rate-1, mul=sd.amp/2, minfreq=sd.freq, maxfreq=sd.freq*2)
    sd.env = Env.perc()

with SynthDef("scatter") as sd:
    sd.osc = (Saw.ar( sd.freq , mul=sd.amp / 8) + VarSaw.ar([sd.freq + 2,sd.freq +1], mul=sd.amp/8)) * LFNoise0.ar(sd.rate)
    sd.env = Env.linen(0.01, sd.sus/2, sd.sus/2)

with SynthDef("charm") as sdef:
    sdef.osc = SinOsc.ar([sdef.freq, sdef.freq + 2 * 2], mul=sdef.amp / 4) + VarSaw.ar(sdef.freq * 8, 10, mul=sdef.amp/8)
    sdef.osc = LPF.ar(sdef.osc, SinOsc.ar(Line.ar(1,sdef.rate*4, sdef.sus/8),0,sdef.freq*2,sdef.freq*2 + 10 ))

with SynthDef("bell") as b:
    b.defaults.update(verb = 0.5)
    b.amp = b.amp * 4
    b.sus = 2.5
    b.osc = Klank.ar([ [0.501, 1, 0.7,   2.002, 3, 9.6,   2.49, 11, 2.571,  3.05, 6.242, 12.49, 13, 16, 24],
                       [0.002,0.02,0.001, 0.008,0.02,0.004, 0.02,0.04,0.02, 0.005,0.05,0.05, 0.02, 0.03, 0.04],
                       stutter([1.2, 0.9, 0.25, 0.14, 0.07], 3) ], Impulse.ar(0.25), b.freq, 0, 3)
    b.env = Env.block()

with SynthDef("soprano") as s:
    s.defaults.update(vib=5, verb=0.5)
    s.amp = s.amp / 2
    s.osc = SinOsc.ar(s.freq * 3, mul=s.amp) + SinOscFB.ar(s.freq * 3, mul=s.amp / 2)
    s.env = Env()

with SynthDef("dub") as d:
    d.freq = d.freq / 4
    d.amp  = d.amp * 2
    d.osc  = LFTri.ar(d.freq, mul=d.amp) + SinOscFB.ar(d.freq, mul=d.amp)
    d.env  = Env.sine(dur=d.sus)

with SynthDef("viola") as v:
    v.defaults.update(verb=0.33, vib=6)
    v.osc = PMOsc.ar(v.freq, Vibrato.kr(v.freq, rate=v.vib, depth=0.008, delay=v.sus*0.25), 10, mul=v.amp / 2)
    v.env = Env.perc( 1/4 * v.sus, 5/2 * v.sus )

with SynthDef("scratch") as s:
    s.defaults.update(depth=0.5, rate=0.04)
    s.freq = s.freq * Crackle.ar(1.5)
    s.osc  = SinOsc.ar(Vibrato.kr(s.freq, 2, 3, rateVariation=s.rate, depthVariation=s.depth), mul=s.amp )
    s.env  = Env()

with SynthDef("klank") as k:
    k.sus = k.sus * 1.5
    k.osc = Klank.ar([[1,2,3,4],[1,1,1,1],[2,2,2,2]], ClipNoise.ar(0.0005).dup, k.freq)
    k.env = Env()

with SynthDef("pluck") as p:
    freq = instance('freq')
    p.amp  = p.amp + 0.00001
    p.freq = [p.freq, p.freq + LFNoise2.ar(50).range(-2,2)]
    p.osc  = SinOsc.ar(freq * 1.002, phase=VarSaw.ar(freq, width=Line.ar(1,0.2,2))) * 0.3 + SinOsc.ar(freq, phase=VarSaw.ar(freq, width=Line.ar(1,0.2,2))) * 0.3
    p.osc  = p.osc * XLine.ar(p.amp, p.amp/10000, p.sus * 4) * 0.3
    p.env  = Env.block(sus=p.sus*1.5)


r = SynthDef("ripple")
r.amp = r.amp / 6
r.osc = Pulse.ar([r.freq/4, r.freq/4+1 ],0.2,0.25) + Pulse.ar([r.freq+2,r.freq],0.5,0.5)
r.osc = r.osc * SinOsc.ar(r.rate/r.sus,0,0.5,1)
r.env = Env(sus=[0.55,0.55])
r.add()

r = SynthDef("rev")
r.amp = r.amp / 4
r.osc = PMOsc.ar(r.freq, r.freq * 2, 10)
r.env = Env.reverse()
r.add()

o = SynthDef("orient")
o.defaults.update(room=10, verb=0.7)
o.osc = LFPulse.ar(o.freq, 0.5, 0.25, 1/4) + LFPulse.ar(o.freq, 1, 0.1, 1/4)
o.env = Env.perc()
o.add()

zap = SynthDef("zap")
zap.defaults.update(room=0, verb=0)
zap.amp = zap.amp / 10
zap.osc = Saw.ar( zap.freq * [1, 1.01] + LFNoise2.ar(50).range(-2,2) ) + VarSaw.ar( zap.freq + LFNoise2.ar(50).range(-2,2), 1 )
zap.env = Env.perc(atk=0.025, curve=-10)
zap.add()

marimba = SynthDef("marimba")
marimba.osc = Klank.ar([[1/2, 1, 4, 9], [1/2,1,1,1], [1,1,1,1]], PinkNoise.ar([0.007, 0.007]), [marimba.freq, marimba.freq], [0,2])
marimba.sus = 1
marimba.env = Env.perc(atk=0.001, curve=-6)
marimba.add()


test = SynthDef("fuzz")
test.freq = test.freq / 2
test.amp = test.amp / 6
test.osc = LFSaw.ar(LFSaw.kr(test.freq,0,test.freq,test.freq * 2))
test.env = Env.block()
test.add()

a = SynthDef("bug")
a.amp = a.amp / 4
a.osc = Pulse.ar([a.freq, a.freq * 1.0001], width=[0.09,0.16,0.25]) * SinOsc.ar(a.rate * 4)
a.env = Env.perc(a.sus * 1.5)
a.add()

p = SynthDef("pulse")
p.amp = p.amp / 4
p.osc = Pulse.ar(p.freq)
p.env = Env.block()
p.add()

p = SynthDef("saw")
p.amp = p.amp / 4
p.osc = Saw.ar(p.freq)
p.env = Env.block()
p.add()
