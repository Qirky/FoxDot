from __future__ import division
from SCLang import *
from SynthDef import SynthDef, SampleSynthDef
import Env

# Sample Player

with SampleSynthDef("play1") as play:
    play.defaults.update(room=0.1 ,rate=1)
    play.rate = play.scrub * LFPar.kr(play.scrub / 4) + play.rate - play.scrub
    play.osc  = PlayBuf.ar(1, play.buf, BufRateScale.ir(play.buf) * play.rate, doneAction=2)
    play.osc  = play.osc * play.amp

with SampleSynthDef("play2") as play:
    play.defaults.update(room=0.1 ,rate=1)
    play.rate = play.scrub * LFPar.kr(play.scrub / 4) + play.rate - play.scrub
    play.osc  = PlayBuf.ar(2, play.buf, BufRateScale.ir(play.buf) * play.rate , doneAction=2)
    play.osc  = play.osc * play.amp

# Synth Players

with SynthDef("pads") as pads:
    pads.amp = pads.amp / 2
    pads.osc = SinOsc.ar([pads.freq, pads.freq + 2], mul=pads.amp)
    pads.env = Env.perc()

with SynthDef("noise") as noise:
    noise.osc = LFNoise0.ar(noise.freq, noise.amp)
    noise.env = Env.env()

with SynthDef("dab") as synth:
     a = HPF.ar(Saw.ar(synth.freq / 4, mul=synth.amp / 2), 2000)
     b = VarSaw.ar(synth.freq / 4, mul=synth.amp, width=Env.perc(synth.sus / 20, synth.sus / 4, 0.5, -5, doneAction=0))
     synth.osc = a + b
     synth.env = Env.env(sus=[Env.sus * 0.25, Env.sus * 1], curve="'lin'")
dab = synth

with SynthDef("varsaw") as synth:
     synth.osc = VarSaw.ar([synth.freq, synth.freq * 1.005], mul=synth.amp / 4, width=synth.rate)
     synth.env = Env.env()
varsaw = synth
    

with SynthDef("growl") as growl:
    growl.sus = growl.sus * 1.5
    growl.osc = SinOsc.ar(growl.freq + SinOsc.kr(0.5, add=1, mul=2), mul=growl.amp) * Saw.ar((growl.sus / 1.5) * 32)
    growl.env = Env.env()

with SynthDef("bass") as bass:
    bass.amp  = bass.amp
    bass.freq = bass.freq / 4
    bass.osc  = LFTri.ar(bass.freq, mul=bass.amp) + VarSaw.ar(bass.freq, width=0.85, mul=bass.amp) + SinOscFB.ar(bass.freq, mul=bass.amp / 2)
    bass.env  = Env.perc(curve="'lin'")

with SynthDef("dirt") as dirt:
    dirt.freq = dirt.freq / 4
    dirt.amp  = dirt.amp / 2
    dirt.osc  = LFSaw.ar(dirt.freq, mul=dirt.amp) + VarSaw.ar(dirt.freq + 1, width=0.85, mul=dirt.amp) + SinOscFB.ar(dirt.freq - 1, mul=dirt.amp/2)
    dirt.env  = Env.perc()

with SynthDef("crunch") as crunch:
    crunch.amp = crunch.amp * 0.5
    crunch.osc = LFNoise0.ar(Crackle.kr(1.95) * crunch.freq * 15, mul=crunch.amp)
    crunch.env = Env.perc(0.01,0.1, crunch.amp / 4)

with SynthDef("rave") as rave:
    rave.osc = Gendy1.ar(rave.rate-1, mul=rave.amp/2, minfreq=rave.freq, maxfreq=rave.freq*2)
    rave.env = Env.perc()

with SynthDef("scatter") as scatter:
    scatter.osc = (Saw.ar( scatter.freq , mul=scatter.amp / 8) + VarSaw.ar([scatter.freq + 2,scatter.freq +1],  mul=scatter.amp/8)) * LFNoise0.ar(scatter.rate)
    scatter.env = Env.linen(0.01, scatter.sus/2, scatter.sus/2)

with SynthDef("charm") as charm:
    charm.osc = SinOsc.ar([charm.freq, charm.freq + 2 * 2], mul=charm.amp / 4) + VarSaw.ar(charm.freq * 8, 10, mul=charm.amp/8)
    charm.osc = LPF.ar(charm.osc, SinOsc.ar(Line.ar(1,charm.rate*4, charm.sus/8),0,charm.freq*2,charm.freq*2 + 10 ))
    charm.env = Env.perc()

with SynthDef("bell") as bell:
    bell.defaults.update(verb = 0.5, room = 0.5)
    bell.amp = bell.amp * 4
    bell.sus = 2.5
    bell.osc = Klank.ar([ [0.501, 1, 0.7,   2.002, 3, 9.6,   2.49, 11, 2.571,  3.05, 6.242, 12.49, 13, 16, 24],
                       [0.002,0.02,0.001, 0.008,0.02,0.004, 0.02,0.04,0.02, 0.005,0.05,0.05, 0.02, 0.03, 0.04],
                       stutter([1.2, 0.9, 0.25, 0.14, 0.07], 3) ], Impulse.ar(0.25), bell.freq, 0, 3)
    bell.env = Env.ramp()

with SynthDef("soprano") as soprano:
    soprano.defaults.update(vib=5, verb=0.5)
    soprano.amp = soprano.amp / 2
    soprano.osc = SinOsc.ar(soprano.freq * 3, mul=soprano.amp) + SinOscFB.ar(soprano.freq * 3, mul=soprano.amp / 2)
    soprano.env = Env.env()

with SynthDef("dub") as dub:
    dub.freq = dub.freq / 4
    dub.amp  = dub.amp * 2
    dub.osc  = LFTri.ar(dub.freq, mul=dub.amp) + SinOscFB.ar(dub.freq, mul=dub.amp)
    dub.env  = Env.sine(dur=dub.sus)

with SynthDef("viola") as viola:
    viola.defaults.update(verb=0.33, vib=6)
    viola.osc = PMOsc.ar(viola.freq, Vibrato.kr(viola.freq, rate=viola.vib, depth=0.008, delay=viola.sus*0.25), 10, mul=viola.amp / 2)
    viola.env = Env.perc( 1/4 * viola.sus, 3/4 * viola.sus )

with SynthDef("scratch") as scratch:
    scratch.defaults.update(depth=0.5, rate=0.04)
    scratch.freq = scratch.freq * Crackle.ar(1.5)
    scratch.osc  = SinOsc.ar(Vibrato.kr(scratch.freq, 2, 3, rateVariation=scratch.rate, depthVariation=scratch.depth), mul=scratch.amp )
    scratch.env  = Env.env()

with SynthDef("klank") as klank:
    klank.sus = klank.sus * 1.5
    klank.osc = Klank.ar([[1,2,3,4],[1,1,1,1],[2,2,2,2]], ClipNoise.ar(0.0005).dup, klank.freq)
    klank.osc = Decimator.ar(klank.osc, bits=klank.rate - 1)
    klank.env = Env.env(klank.sus*2)

with SynthDef("quin") as synth:
    synth.amp = synth.amp 
    synth.osc = Klank.ar([[1,2,4,2],[100,50,0,10],[1,5,0,1]], Impulse.ar(synth.freq).dup, [synth.freq * 1.01, synth.freq]) / 5000
    synth.osc = synth.osc * LFSaw.ar(synth.freq * synth.rate)
    synth.env = Env.perc(atk=0.01, sus=synth.sus, curve=1)
quin = synth

with SynthDef("pluck") as pluck:
    freq = instance('freq')
    pluck.amp  = pluck.amp + 0.00001
    pluck.freq = [pluck.freq, pluck.freq + LFNoise2.ar(50).range(-2,2)]
    pluck.osc  = SinOsc.ar(freq * 1.002, phase=VarSaw.ar(freq, width=Line.ar(1,0.2,2))) * 0.3 + SinOsc.ar(freq, phase=VarSaw.ar(freq, width=Line.ar(1,0.2,2))) * 0.3
    pluck.osc  = pluck.osc * XLine.ar(pluck.amp, pluck.amp/10000, pluck.sus * 4, doneAction=2) * 0.3

with SynthDef("spark") as synth:
    freq = instance('freq')
    synth.amp  = synth.amp + 0.00001
    synth.freq = [synth.freq, synth.freq + LFNoise2.ar(50).range(-2,2)]
    synth.osc  = LFSaw.ar(freq * 1.002, iphase=Saw.ar(0.1)) * 0.3 + LFSaw.ar(freq, iphase=Saw.ar(0.1)) * 0.3
    synth.osc  = synth.osc * Line.ar(synth.amp, synth.amp/10000, synth.sus * 1.5) * 0.3
spark = synth

with SynthDef("blip") as synth:
    freq = instance('freq')
    synth.amp  = synth.amp + 0.00001
    synth.freq = [synth.freq, synth.freq + LFNoise2.ar(50).range(-2,2)]
    synth.osc  = (LFCub.ar(freq * 1.002, iphase=1.5) + LFTri.ar(freq, iphase=Line.ar(2,0,0,2)) * 0.3) * Blip.ar(freq / 2, synth.rate)
    synth.osc  = synth.osc * XLine.ar(synth.amp, synth.amp/10000, synth.sus * 2) * 0.3
blip = synth


with SynthDef("ripple") as ripple:
    ripple.amp = ripple.amp / 6
    ripple.osc = Pulse.ar([ripple.freq/4, ripple.freq/4+1 ],0.2,0.25) + Pulse.ar([ripple.freq+2,ripple.freq],0.5,0.5)
    ripple.osc = ripple.osc * SinOsc.ar(ripple.rate/ripple.sus,0,0.5,1)
    ripple.env = Env.env(sus=[0.55,0.55])

with SynthDef("creep") as creep:
    creep.amp = creep.amp / 4
    creep.osc = PMOsc.ar(creep.freq, creep.freq * 2, 10)
    creep.env = Env.reverse()

# No context manager SynthDef creation

orient = SynthDef("orient")
orient.defaults.update(room=10, verb=0.7)
orient.osc = LFPulse.ar(orient.freq, 0.5, 0.25, 1/4) + LFPulse.ar(orient.freq, 1, 0.1, 1/4)
orient.env = Env.perc()
orient.add()

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

fuzz = SynthDef("fuzz")
fuzz.freq = fuzz.freq / 2
fuzz.amp = fuzz.amp / 6
fuzz.osc = LFSaw.ar(LFSaw.kr(fuzz.freq,0,fuzz.freq,fuzz.freq * 2))
fuzz.env = Env.ramp()
fuzz.add()

bug = SynthDef("bug")
bug.amp = bug.amp / 5
bug.osc = Pulse.ar([bug.freq, bug.freq * 1.0001], width=[0.09,0.16,0.25]) * SinOsc.ar(bug.rate * 4)
bug.env = Env.perc(bug.sus * 1.5)
bug.add()

pulse = SynthDef("pulse")
pulse.amp = pulse.amp / 4
pulse.osc = Pulse.ar(pulse.freq)
pulse.env = Env.mask()
pulse.add()

saw = SynthDef("saw")
saw.amp = saw.amp / 4
saw.osc = Saw.ar(saw.freq)
saw.env = Env.mask()
saw.add()

snick = SynthDef("snick")
snick.osc = LFPar.ar(snick.freq, mul=1) * Blip.ar(((snick.rate+1) * 4))
snick.env = Env.perc()
snick.add()

twang = SynthDef("twang")
twang.freq = twang.freq / 2
twang.osc = LPF.ar(Impulse.ar([twang.freq, twang.freq + 1]), 4000)
twang.osc = CombL.ar(twang.osc, delaytime=[0.004,0.003], maxdelaytime= 2);
twang.env = Env.perc()
twang.add()

donk = SynthDef("donk")
donk.amp = donk.amp * 9
donk.freq = donk.freq / 4
donk.osc = Ringz.ar(Impulse.ar(0), [donk.freq, donk.freq + 2], donk.sus, donk.amp)
donk.add()

squish = SynthDef("squish")
squish.freq = squish.freq / 4
squish.osc = Ringz.ar(Pulse.ar(4 * squish.rate), squish.freq, squish.sus, squish.amp)
squish.osc = squish.osc * XLine.ar(1/2, 0.000001, squish.sus, doneAction=2)
squish.osc = squish.osc.cos
squish.add()

# Get rid of the variable synth

del synth
