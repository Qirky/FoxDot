SynthDef.new(\distortion,
{|bus, shape|
var osc;
osc = In.ar(bus, 2);
osc = osc;
ReplaceOut.ar(bus, osc)}).add;