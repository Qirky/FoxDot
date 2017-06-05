SynthDef.new(\formantFilter,
{|bus, formant|
var osc;
osc = In.ar(bus, 2);
formant = (formant % 8) + 1;
osc = Formlet.ar(osc, formant * 200, formant / 1000, formant / 500).tanh;
ReplaceOut.ar(bus, osc)}).add;