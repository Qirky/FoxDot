SynthDef.new(\bass,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=8, bus=0, blur=1, beat_dur=1, atk=0.01, decay=0.01, rel=0.01, peak=1, level=0.8|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 4);
amp=(amp * 0.8);
osc=((LFTri.ar(freq, mul: amp) + VarSaw.ar(freq, width: (rate / 10), mul: amp)) + SinOscFB.ar(freq, mul: (amp / 2)));
env=EnvGen.ar(Env.perc(attackTime: 0.02,releaseTime: sus,level: amp,curve: 'lin'), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
