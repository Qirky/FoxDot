SynthDef.new(\viola,
{|amp=1, verb=0.33, freq=0, pan=0, rate=0, vib=6, sus=1, fmod=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 2);
osc=PMOsc.ar(freq, Vibrato.kr(freq, rate: vib, delay: (sus * 0.25), depth: 0.008), 10, mul: (amp / 2));
env=EnvGen.ar(Env.perc(attackTime: (0.25 * sus),releaseTime: (0.75 * sus),curve: 0,level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
