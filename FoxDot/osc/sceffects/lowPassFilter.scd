SynthDef.new(\lowPassFilter,
{|bus, lpf, lpr|
var osc;
osc = In.ar(bus, 2);
osc = RLPF.ar(osc, lpf, lpr);
ReplaceOut.ar(bus, osc)}).add;