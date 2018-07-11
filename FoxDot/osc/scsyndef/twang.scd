SynthDef.new(\twang,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 8);
freq=(freq + [0, 2]);
osc=LPF.ar(Impulse.ar(freq, 0.1), 4000);
osc=(EnvGen.ar(Env.perc(level: amp,curve: 0,releaseTime: sus,attackTime: 0.01), doneAction: 0) * CombL.ar(osc, delaytime: (rate / (freq * 8)), maxdelaytime: 0.25));
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
