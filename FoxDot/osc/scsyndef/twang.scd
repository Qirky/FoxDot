SynthDef.new(\twang,
{|vib=0, bus=0, fmod=0, sus=1, amp=1, rate=0, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 8);
freq=(freq + [0, 2]);
osc=LPF.ar(Impulse.ar(freq, 0.1), 4000);
osc=(EnvGen.ar(Env.perc(releaseTime: sus,curve: 0,attackTime: 0.01,level: amp), doneAction: 0) * CombL.ar(osc, maxdelaytime: 0.25, delaytime: (rate / (freq * 8))));
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
