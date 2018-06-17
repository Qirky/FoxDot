SynthDef.new(\bug,
{|amp=1, freq=0, pan=0, rate=1, vib=0, sus=1, fmod=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 5);
freq=(freq * [1, 1.0001]);
osc=(Pulse.ar(freq, width: [0.09, 0.16, 0.25]) * SinOsc.ar((rate * 4)));
env=EnvGen.ar(Env.perc(attackTime: (sus * 1.5),releaseTime: sus,curve: 0,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
