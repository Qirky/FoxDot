SynthDef.new(\lowPassFilter,
{|bus, lpr, lpf|
var osc;
osc = In.ar(bus, 2);
osc = RLPF.ar(osc, lpf, lpr);
ReplaceOut.ar(bus, osc)}).add;