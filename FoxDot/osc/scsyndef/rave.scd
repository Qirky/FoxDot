SynthDef.new(\rave,
{|amp=1, freq=0, pan=0, rate=0, vib=0, sus=1, fmod=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=Gendy1.ar((rate - 1), maxfreq: (freq * 2), mul: (amp / 2), minfreq: freq);
env=EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: sus,curve: 0,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
