SynthDef.new(\dirtortion,
{|bus, distort|
var osc;
osc = In.ar(bus, 2);
osc = CrossoverDistortion.ar(osc, amp: distort);
ReplaceOut.ar(bus, osc)}).add;