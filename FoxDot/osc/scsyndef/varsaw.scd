SynthDef.new(\varsaw,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=(freq * [1, 1.005]);
osc=VarSaw.ar(freq, mul: (amp / 4), width: rate);
env=EnvGen.ar(Env(times: [(sus / 2), (sus / 2)],curve: 'lin',levels: [0, amp, 0]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
