SynthDef.new(\growl,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
sus=(sus * 1.5);
osc=(SinOsc.ar((freq + SinOsc.kr(0.5, add: 1, mul: 2)), mul: amp) * Saw.ar(((sus / 1.5) * 32)));
env=EnvGen.ar(Env(times: [(sus / 2), (sus / 2)],curve: 'lin',levels: [0, amp, 0]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
