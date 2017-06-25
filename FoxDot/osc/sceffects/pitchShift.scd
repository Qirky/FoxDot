SynthDef.new(\pitchShift,
{|bus, shift|
var osc;
osc = In.ar(bus, 2);
osc = PitchShift.ar(osc, 0.02, shift);
ReplaceOut.ar(bus, osc)}).add;