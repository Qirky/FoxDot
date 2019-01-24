SynthDef.new(\arpy,
{|vib=0, rel=0.01, bus=0, rate=0, peak=1, amp=1, freq=0, beat_dur=1, decay=0.01, level=0.8, atk=0.01, sus=1, fmod=0, blur=1, pan=0|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq / 2);
amp=(amp * 2);
freq=(freq + [0, 0.5]);
osc=LPF.ar(Impulse.ar(freq), 3000);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.01,releaseTime: (sus * 0.25)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
