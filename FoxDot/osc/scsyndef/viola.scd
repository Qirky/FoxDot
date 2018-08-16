SynthDef.new(\viola,
{|vib=6, beat_dur=1, bus=0, rate=0, verb=0.33, sus=1, fmod=0, blur=1, amp=1, freq=0, pan=0|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 2);
osc=PMOsc.ar(freq, Vibrato.kr(freq, delay: (sus * 0.25), rate: vib, depth: 0.008), 10, mul: (amp / 2));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: (0.25 * sus),releaseTime: (0.75 * sus)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
