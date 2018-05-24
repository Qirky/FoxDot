SynthDef.new(\donk,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
freq=((freq / 2) + [0, 2]);
amp=(amp / 1.25);
osc=Ringz.ar((Impulse.ar(0, phase: rate) / (rate + 1)), freq, sus, amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
