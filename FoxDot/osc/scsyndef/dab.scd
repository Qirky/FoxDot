SynthDef.new(\dab,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
osc=(HPF.ar(Saw.ar((freq / 4), mul: (amp / 2)), 2000) + VarSaw.ar((freq / 4), mul: amp, width: EnvGen.ar(Env.perc(level: 0.5,curve: -5,attackTime: (sus / 20),releaseTime: (sus / 4)), doneAction: 0)));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus * 0.25), (sus * 1)]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
