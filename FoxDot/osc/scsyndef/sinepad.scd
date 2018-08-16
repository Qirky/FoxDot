SynthDef.new(\sinepad,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, blur=1, beat_dur=1|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp * 1.5);
freq=(freq + [0, 2]);
osc=SinOsc.ar(freq, mul: amp);
osc=HPF.ar(osc, 1000);
env=EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: sus,level: amp,curve: 0), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
