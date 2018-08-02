SynthDef.new(\marimba,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, blur=1, beat_dur=1|
var osc, env;
sus = sus * blur * beat_dur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=Klank.ar(`[[0.5, 1, 4, 9], [0.5, 1, 1, 1], [1, 1, 1, 1]], PinkNoise.ar([0.007, 0.007]), freq, [0, 2]);
sus=1;
env=EnvGen.ar(Env.perc(attackTime: 0.001,releaseTime: sus,level: amp,curve: -6), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
