SynthDef.new(\charm,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
osc=(SinOsc.ar([freq, (freq + 4)], mul: (amp / 4)) + VarSaw.ar((freq * 8), 10, mul: (amp / 8)));
osc=LPF.ar(osc, SinOsc.ar(Line.ar(1, (rate * 4), (sus / 8)), 0, (freq * 2), ((freq * 2) + 10)));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.01,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
