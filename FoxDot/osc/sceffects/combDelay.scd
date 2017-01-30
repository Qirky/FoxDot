SynthDef.new(\combDelay,
{|bus, echo|
var osc;
osc = In.ar(bus, 2);
osc = osc + CombL.ar(osc, delaytime: echo, maxdelaytime: 2);
ReplaceOut.ar(bus, osc)}).add;