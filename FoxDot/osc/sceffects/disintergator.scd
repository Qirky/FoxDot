SynthDef.new(\disintergator,
{|bus, grate|
var osc;
osc = In.ar(bus, 2);
osc = Disintegrator.ar(osc, multiplier: grate);
ReplaceOut.ar(bus, osc)}).add;