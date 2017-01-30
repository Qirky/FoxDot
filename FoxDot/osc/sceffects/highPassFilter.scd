SynthDef.new(\highPassFilter,
{|bus, hpf|
var osc;
osc = In.ar(bus, 2);
osc = HPF.ar(osc, hpf);
ReplaceOut.ar(bus, osc)}).add;