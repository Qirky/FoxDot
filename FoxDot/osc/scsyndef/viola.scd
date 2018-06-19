SynthDef.new(\viola,
{|vib=6, bus=0, fmod=0, sus=1, amp=1, rate=0, verb=0.33, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 2);
osc=PMOsc.ar(freq, Vibrato.kr(freq, depth: 0.008, delay: (sus * 0.25), rate: vib), 10, mul: (amp / 2));
env=EnvGen.ar(Env.perc(releaseTime: (0.75 * sus),curve: 0,attackTime: (0.25 * sus),level: amp), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
