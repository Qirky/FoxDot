SynthDef.new(\bitcrush,
{|bus, crush, sus, bits, amp|
var osc;
osc = In.ar(bus, 2);
osc = Decimator.ar(osc, rate: 44100/crush, bits: bits);
osc = osc * Line.ar(amp * 0.85, 0.0001, sus * 2);
ReplaceOut.ar(bus, osc)}).add;