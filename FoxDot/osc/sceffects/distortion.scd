SynthDef.new(\distortion,
{|bus, dist|
var osc;
osc = In.ar(bus, 2);
osc = CrossoverDistortion.ar(osc, smooth:1-dist);
ReplaceOut.ar(bus, osc)}).add;