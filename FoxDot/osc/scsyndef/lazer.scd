SynthDef.new(\lazer,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=(amp * 0.1);
osc=(VarSaw.ar([freq, (freq * 1.005)], width: ((rate - 1) / 4)) + LFSaw.ar(LFNoise0.ar((rate * 20), mul: 0.5, add: (freq * Pulse.ar(((rate - 2) + 0.1), add: 1)))));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.1,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
