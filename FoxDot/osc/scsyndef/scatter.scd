SynthDef.new(\scatter,
{|vib=0, rel=0.01, bus=0, rate=0, peak=1, amp=1, freq=0, beat_dur=1, decay=0.01, level=0.8, atk=0.01, sus=1, fmod=0, blur=1, pan=0|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=((Saw.ar(freq, mul: (amp / 8)) + VarSaw.ar((freq + [2, 1]), mul: (amp / 8))) * LFNoise0.ar(rate));
env=EnvGen.ar(Env.linen(level: (sus / 2),curve: 0,attackTime: 0.01,releaseTime: (sus / 2)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
