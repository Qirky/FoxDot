SynthDef.new(\varsaw,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, blur=1, beat_dur=1, pan=0|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq * [1, 1.005]);
osc=VarSaw.ar(freq, mul: (amp / 4), width: rate);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
