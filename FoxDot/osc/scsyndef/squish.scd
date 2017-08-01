SynthDef.new(\squish,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
freq=(freq / 4);
osc=Ringz.ar(Pulse.ar((4 * rate)), freq, sus, amp);
osc=(osc * XLine.ar(0.5, 1e-06, sus, doneAction: 2));
osc=osc.cos;
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
