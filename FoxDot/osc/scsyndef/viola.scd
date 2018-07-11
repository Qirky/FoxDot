SynthDef.new(\viola,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=6, verb=0.33|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 2);
osc=PMOsc.ar(freq, Vibrato.kr(freq, rate: vib, delay: (sus * 0.25), depth: 0.008), 10, mul: (amp / 2));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,releaseTime: (0.75 * sus),attackTime: (0.25 * sus)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
