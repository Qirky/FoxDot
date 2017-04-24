SynthDef.new(\lowPassFilter,
{|bus, lpf, resonance|
var osc;
osc = In.ar(bus, 2);
osc = RLPF.ar(osc, lpf, resonance);
ReplaceOut.ar(bus, osc)}).add;