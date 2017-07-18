SynthDef.new(\pitchShift,
{|bus, pshift|
var osc;
osc = In.kr(bus, 1);
osc = osc * (1.059463**pshift);
ReplaceOut.kr(bus, osc)}).add;