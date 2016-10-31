SynthDef.new(\marimba,
{|vib=0, grain=0, echoOn=0, scrub=0, room=0.3, chop=0, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0.25, sus=1, slidefrom=1, fmod=0, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
sus=1;
osc=Decimator.ar((LPF.ar(HPF.ar(Klank.ar(`[[0.5, 1, 4, 9], [0.5, 1, 1, 1], [1, 1, 1, 1]], PinkNoise.ar([0.007, 0.007]), [freq, freq], [0, 2]), hpf), (lpf + 1)) * LFPulse.ar((chop / 1))), rate: 44100, bits: bits);
env=EnvGen.ar(Env.perc(attackTime: 0.001, level: amp, curve: -6, releaseTime: sus), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;