SynthDef.new(\chop,
{|bus, chop, sus|
var osc;
osc = In.ar(bus, 2);
osc = osc * LFPulse.ar(chop / sus, add: 0.1);
ReplaceOut.ar(bus, osc)}).add;