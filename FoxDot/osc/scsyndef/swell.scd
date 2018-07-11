SynthDef.new(\swell,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=1, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 4);
freq=(freq + [0, 1]);
freq=(freq * [1, 0.5]);
osc=VarSaw.ar(freq, width: SinOsc.ar((rate / ((2 * sus) / 1.25)), add: 0.5, mul: [0.5, 0.5]), mul: [1, 0.5]);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,releaseTime: sus,attackTime: 0.01), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
