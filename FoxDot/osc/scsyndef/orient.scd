SynthDef.new(\orient,
{|vib=0, bus=0, fmod=0, sus=1, amp=1, rate=0, verb=0.7, freq=0, room=10, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=(LFPulse.ar(freq, 0.5, 0.25, 0.25) + LFPulse.ar(freq, 1, 0.1, 0.25));
env=EnvGen.ar(Env.perc(releaseTime: sus,curve: 0,attackTime: 0.01,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
