SynthDef.new(\quin,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
osc=(Klank.ar(`[[1, 2, 4, 2], [100, 50, 0, 10], [1, 5, 0, 1]], Impulse.ar(freq).dup, [(freq * 1.01), freq]) / 5000);
osc=(osc * LFSaw.ar((freq * (1 + rate))));
env=EnvGen.ar(Env.perc(level: amp,curve: 1,attackTime: 0.01,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
