SynthDef.new(\swell,
{|amp=1, freq=0, pan=0, rate=1, vib=0, sus=1, fmod=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 4);
freq=(freq + [0, 1]);
freq=(freq * [1, 0.5]);
osc=VarSaw.ar(freq, mul: [1, 0.5], width: SinOsc.ar((rate / ((2 * sus) / 1.25)), mul: [0.5, 0.5], add: 0.5));
env=EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: sus,curve: 0,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
