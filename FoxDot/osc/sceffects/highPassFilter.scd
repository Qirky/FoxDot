SynthDef.new(\highPassFilter,
{|bus, hpr, hpf|
var osc;
osc = In.ar(bus, 2);
osc = RHPF.ar(osc, hpf, hpr);
ReplaceOut.ar(bus, osc)}).add;