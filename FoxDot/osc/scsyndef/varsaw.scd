SynthDef.new(\varsaw,
{|pan=0, sus=1, rate=0, vib=0, fmod=0, freq=0, amp=1, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq * [1, 1.005]);
osc=VarSaw.ar(freq, width: rate, mul: (amp / 4));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
