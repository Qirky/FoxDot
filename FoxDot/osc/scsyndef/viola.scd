SynthDef.new(\viola,
{|amp=1, sus=1, pan=0, freq=0, vib=6, fmod=0, rate=0, bus=0, blur=1, beat_dur=1, atk=0.01, decay=0.01, rel=0.01, peak=1, level=0.8, verb=0.33|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 2);
osc=PMOsc.ar(freq, Vibrato.kr(freq, rate: vib, depth: 0.008, delay: (sus * 0.25)), 10, mul: (amp / 2));
env=EnvGen.ar(Env.perc(attackTime: (0.25 * sus),releaseTime: (0.75 * sus),level: amp,curve: 0), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
