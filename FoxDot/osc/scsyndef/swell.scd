SynthDef.new(\swell,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=(amp / 4);
osc=VarSaw.ar([freq, ((freq + 1) / 0.75)], width: SinOsc.ar((rate / ((2 * sus) / 1.25)), mul: [0.5, 0.5], add: 0.5), mul: [1, 0.5]);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.01,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
