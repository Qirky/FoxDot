SynthDef.new(\bitcrush,
{|bus, bits, sus, amp|
var osc;
osc = In.ar(bus, 2);
osc = Decimator.ar(osc, rate: 44100, bits: bits);
osc = osc * Line.ar(amp * 0.5, 0.0001, sus);
ReplaceOut.ar(bus, osc)}).add;