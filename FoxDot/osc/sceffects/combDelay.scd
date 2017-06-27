SynthDef.new(\combDelay,
{|bus, decay, sus, echo|
var osc;
osc = In.ar(bus, 2);
osc = osc + CombL.ar(osc, delaytime: echo * sus, maxdelaytime: 2, decaytime: decay);
ReplaceOut.ar(bus, osc)}).add;