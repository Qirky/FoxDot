SynthDef.new(\donk,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
freq=(freq / 2);
amp=(amp / 1.25);
osc=Ringz.ar((Impulse.ar(0, phase: rate) / (rate + 1)), [freq, (freq + 2)], sus, amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
