SynthDef.new(\bass,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=8, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 4);
amp=(amp * 0.8);
osc=((LFTri.ar(freq, mul: amp) + VarSaw.ar(freq, width: (rate / 10), mul: amp)) + SinOscFB.ar(freq, mul: (amp / 2)));
env=EnvGen.ar(Env.perc(level: amp,curve: 'lin',releaseTime: sus,attackTime: 0.02), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
