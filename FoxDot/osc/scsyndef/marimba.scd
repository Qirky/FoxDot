SynthDef.new(\marimba,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=Klank.ar(`[[0.5, 1, 4, 9], [0.5, 1, 1, 1], [1, 1, 1, 1]], PinkNoise.ar([0.007, 0.007]), freq, [0, 2]);
sus=1;
env=EnvGen.ar(Env.perc(level: amp,curve: -6,releaseTime: sus,attackTime: 0.001), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
