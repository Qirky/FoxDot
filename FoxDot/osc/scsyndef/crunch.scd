SynthDef.new(\crunch,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, blur=1, beat_dur=1, atk=0.01, decay=0.01, rel=0.01, peak=1, level=0.8|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp * 0.5);
osc=LFNoise0.ar(((Crackle.kr(1.95) * freq) * 15), mul: amp);
env=EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: 0.1,level: (amp / 4),curve: 0), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
