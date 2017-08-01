SynthDef.new(\zap,
{|vib=0, rate=0, verb=0, sus=1, room=0, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=(amp / 10);
osc=(Saw.ar(((freq * [1, 1.01]) + LFNoise2.ar(50).range(-2, 2))) + VarSaw.ar((freq + LFNoise2.ar(50).range(-2, 2)), 1));
env=EnvGen.ar(Env.perc(level: amp,curve: -10,attackTime: 0.025,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
