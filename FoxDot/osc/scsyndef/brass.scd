SynthDef.new(\brass,
{|vib=0, rate=0.3, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
rate=Lag.ar(freq, rate);
osc=(Saw.ar(rate, 0.4) + Saw.ar((rate + LFNoise2.ar(1).range(0.5, 1.1)), 0.4));
osc=(osc + Resonz.ar(osc, (freq * XLine.ar(1, 5, 0.13)), 1));
osc=BPF.ar(osc, (freq * 2.5), 0.3);
osc=RLPF.ar(osc, 1300, 0.78);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.01,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
