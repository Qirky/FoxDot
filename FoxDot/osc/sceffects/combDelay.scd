SynthDef.new(\combDelay,
{|bus, echo, sus|
var osc;
osc = In.ar(bus, 2);
osc = osc + CombL.ar(osc, delaytime: echo * sus, maxdelaytime: 2);
ReplaceOut.ar(bus, osc)}).add;