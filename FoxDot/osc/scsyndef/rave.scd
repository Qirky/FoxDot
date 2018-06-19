SynthDef.new(\rave,
{|vib=0, bus=0, fmod=0, sus=1, amp=1, rate=0, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=Gendy1.ar((rate - 1), maxfreq: (freq * 2), minfreq: freq, mul: (amp / 2));
env=EnvGen.ar(Env.perc(releaseTime: sus,curve: 0,attackTime: 0.01,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
