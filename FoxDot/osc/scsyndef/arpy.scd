SynthDef.new(\arpy,
{|vib=0, bus=0, fmod=0, sus=1, amp=1, rate=0, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 2);
amp=(amp * 2);
freq=(freq + [0, 0.5]);
osc=LPF.ar(Impulse.ar(freq), 3000);
env=EnvGen.ar(Env.perc(releaseTime: (sus * 0.25),curve: 0,attackTime: 0.01,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
