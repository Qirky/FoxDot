SynthDef.new(\zap,
{|amp=1, verb=0, room=0, freq=0, pan=0, rate=0, vib=0, sus=1, fmod=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 10);
osc=(Saw.ar(((freq * [1, 1.01]) + LFNoise2.ar(50).range(-2, 2))) + VarSaw.ar((freq + LFNoise2.ar(50).range(-2, 2)), 1));
env=EnvGen.ar(Env.perc(attackTime: 0.025,releaseTime: sus,curve: -10,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
