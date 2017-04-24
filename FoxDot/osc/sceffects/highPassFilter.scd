SynthDef.new(\highPassFilter,
{|bus, hpf, resonance|
var osc;
osc = In.ar(bus, 2);
osc = RHPF.ar(osc, hpf, resonance);
ReplaceOut.ar(bus, osc)}).add;