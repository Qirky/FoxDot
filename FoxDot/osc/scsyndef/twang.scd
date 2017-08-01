SynthDef.new(\twang,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
freq=(freq / 8);
osc=LPF.ar(Impulse.ar([freq, (freq + 2)], 0.1), 4000);
osc=(EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.01,releaseTime: sus), doneAction: 0) * CombL.ar(osc, delaytime: (rate / (freq * 8)), maxdelaytime: 0.25));
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
