SynthDef.new(\arpy,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
freq=(freq / 2);
amp=(amp * 2);
osc=LPF.ar(Impulse.ar([freq, (freq + 0.5)]), 3000);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.01,releaseTime: (sus * 0.25)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
