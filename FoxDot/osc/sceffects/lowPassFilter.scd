SynthDef.new(\lowPassFilter,
{|bus, lpf|
var osc;
osc = In.ar(bus, 2);
osc = LPF.ar(osc, lpf);
ReplaceOut.ar(bus, osc)}).add;