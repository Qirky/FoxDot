SynthDef.new(\bass,
{|vib=0, rate=8.5, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 4);
osc=((LFTri.ar(freq, mul: amp) + VarSaw.ar(freq, width: (rate / 10), mul: amp)) + SinOscFB.ar(freq, mul: (amp / 2)));
env=EnvGen.ar(Env.perc(level: amp,curve: 'lin',attackTime: 0.02,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
