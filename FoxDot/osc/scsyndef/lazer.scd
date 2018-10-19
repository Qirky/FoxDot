SynthDef.new(\lazer,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, blur=1, beat_dur=1, atk=0.01, decay=0.01, rel=0.01, peak=1, level=0.8|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq * [1, 1.005]);
amp=(amp * 0.1);
osc=(VarSaw.ar(freq, width: ((rate - 1) / 4)) + LFSaw.ar(LFNoise0.ar((rate * 20), add: (freq * Pulse.ar(((rate - 2) + 0.1), add: 1)), mul: 0.5)));
env=EnvGen.ar(Env.perc(attackTime: 0.1,releaseTime: sus,level: amp,curve: 0), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
