SynthDef.new(\wavesShapeDistortion,
{|bus, shape|
var osc;
osc = In.ar(bus, 2);
osc = (osc * (shape * 50)).fold2(1).distort / 5;
ReplaceOut.ar(bus, osc)}).add;