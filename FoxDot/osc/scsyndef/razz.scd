SynthDef.new(\razz,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0.3, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq + [0, 1]);
rate=Lag.ar(K2A.ar(freq), rate);
osc=(Saw.ar((rate * [1, 0.5]), [1, 0.3333333333333333]) + Saw.ar((rate + LFNoise2.ar(4).range(0.5, 2.5)), 1));
osc=BPF.ar(osc, (freq * 2.5), 0.3);
osc=RLPF.ar(osc, 1300, 0.78);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,releaseTime: sus,attackTime: 0.125), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
