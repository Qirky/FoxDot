SynthDef.new(\bass,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 4);
osc=((LFTri.ar(freq, mul: amp) + VarSaw.ar(freq, width: 0.85, mul: amp)) + SinOscFB.ar(freq, mul: (amp / 2)));
env=EnvGen.ar(Env.perc(level: amp,curve: 'lin',attackTime: 0.01,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
