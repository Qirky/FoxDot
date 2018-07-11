SynthDef.new(\rave,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=Gendy1.ar((rate - 1), maxfreq: (freq * 2), mul: (amp / 2), minfreq: freq);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,releaseTime: sus,attackTime: 0.01), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
