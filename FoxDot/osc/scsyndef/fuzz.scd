SynthDef.new(\fuzz,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
freq=(freq / 2);
amp=(amp / 6);
osc=LFSaw.ar(LFSaw.kr(freq, 0, freq, (freq * 2)));
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1), (amp * 0.01)],curve: 'step',times: [(sus * 0.8), 0.01]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
