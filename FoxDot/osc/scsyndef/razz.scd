SynthDef.new(\razz,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0.3, bus=0, blur=1, beat_dur=1, atk=0.01, decay=0.01, rel=0.01, peak=1, level=0.8|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq + [0, 1]);
rate=Lag.ar(K2A.ar(freq), rate);
osc=(Saw.ar((rate * [1, 0.5]), [1, 0.3333333333333333]) + Saw.ar((rate + LFNoise2.ar(4).range(0.5, 2.5)), 1));
osc=BPF.ar(osc, (freq * 2.5), 0.3);
osc=RLPF.ar(osc, 1300, 0.78);
env=EnvGen.ar(Env.perc(attackTime: 0.125,releaseTime: sus,level: amp,curve: 0), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
