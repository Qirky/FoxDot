SynthDef.new(\crunch,
{|pan=0, sus=1, rate=0, vib=0, fmod=0, freq=0, amp=1, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp * 0.5);
osc=LFNoise0.ar(((Crackle.kr(1.95) * freq) * 15), mul: amp);
env=EnvGen.ar(Env.perc(curve: 0,releaseTime: 0.1,level: (amp / 4),attackTime: 0.01), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
