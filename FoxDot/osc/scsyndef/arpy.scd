SynthDef.new(\arpy,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 2);
amp=(amp * 2);
osc=LPF.ar(Impulse.ar([freq, (freq + 0.5)]), 3000);
env=EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: (sus * 0.25),level: amp,curve: 0), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
