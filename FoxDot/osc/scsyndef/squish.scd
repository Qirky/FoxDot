SynthDef.new(\squish,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, bits=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 4);
osc=Ringz.ar(Pulse.ar((4 * rate)), freq, sus, amp);
osc=(osc * XLine.ar(0.5, 1e-06, sus, doneAction: 2));
osc=osc.cos;
osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
	ReplaceOut.ar(bus, osc)}).add;
