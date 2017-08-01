SynthDef.new(\growl,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
sus=(sus * 1.5);
osc=(SinOsc.ar((freq + SinOsc.kr(0.5, mul: 2, add: 1)), mul: amp) * Saw.ar(((sus / 1.5) * 32)));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
