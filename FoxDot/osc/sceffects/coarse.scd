SynthDef.new(\coarse,
{|bus, coarse, sus|
var osc;
osc = In.kr(bus, 1);
osc = osc * LFPulse.ar(coarse / sus);
ReplaceOut.kr(bus, osc)}).add;