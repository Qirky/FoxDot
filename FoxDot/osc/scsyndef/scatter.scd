SynthDef.new(\scatter,
{|amp=1, freq=0, pan=0, rate=0, vib=0, sus=1, fmod=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=((Saw.ar(freq, mul: (amp / 8)) + VarSaw.ar((freq + [2, 1]), mul: (amp / 8))) * LFNoise0.ar(rate));
env=EnvGen.ar(Env.linen(attackTime: 0.01,releaseTime: (sus / 2),curve: 0,level: (sus / 2)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
