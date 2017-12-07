SynthDef.new(\bug,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=1, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 5);
osc=(Pulse.ar([freq, (freq * 1.0001)], width: [0.09, 0.16, 0.25]) * SinOsc.ar((rate * 4)));
env=EnvGen.ar(Env.perc(attackTime: (sus * 1.5),releaseTime: sus,level: amp,curve: 0), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
