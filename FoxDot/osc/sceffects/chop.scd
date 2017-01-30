SynthDef.new(\chop,
{|bus, chop, sus|
var osc;
osc = In.ar(bus, 2);
osc = osc * LFPulse.ar(chop / sus);
ReplaceOut.ar(bus, osc)}).add;