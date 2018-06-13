SynthDef.new(\noise,
{|pan=0, sus=1, rate=0, vib=0, fmod=0, freq=0, amp=1, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq * 2);
osc=LFNoise0.ar(freq, amp);
env=EnvGen.ar(Env.perc(curve: 0,releaseTime: sus,level: amp,attackTime: 0.01), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
