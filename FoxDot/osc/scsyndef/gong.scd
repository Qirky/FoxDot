SynthDef.new(\gong,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=(amp * 4);
freq=(freq * 2);
osc=Klank.ar(`[[0.501, 1, 0.8, 2.002, 3, 9.6, 2.49, 11, 2.571, 3.05, 6.242, 12.49, 13, 16, 24], [0.002, 0.02, 0.001, 0.008, 0.02, 0.004, 0.02, 0.04, 0.02, 0.005, 0.05, 0.05, 0.02, 0.03, 0.04], ([1.2, 1.2, 1.2, 0.9, 0.9, 0.9, 0.25, 0.25, 0.25, 0.14, 0.14, 0.14, 0.07, 0.07, 0.07] * sus)], SinOscFB.ar(20, 0, 10), freq, 0, 4);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 0)],curve: 'lin',times: (sus * 8)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
