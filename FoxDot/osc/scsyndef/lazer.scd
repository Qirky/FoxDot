SynthDef.new(\lazer,
{|vib=0, bus=0, fmod=0, sus=1, amp=1, rate=0, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq * [1, 1.005]);
amp=(amp * 0.1);
osc=(VarSaw.ar(freq, width: ((rate - 1) / 4)) + LFSaw.ar(LFNoise0.ar((rate * 20), add: (freq * Pulse.ar(((rate - 2) + 0.1), add: 1)), mul: 0.5)));
env=EnvGen.ar(Env.perc(releaseTime: sus,curve: 0,attackTime: 0.1,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
