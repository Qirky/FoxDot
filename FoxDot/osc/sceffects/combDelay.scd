SynthDef.new(\combDelay,
{|bus, echo, sus, decay|
var osc;
osc = In.ar(bus, 2);
osc = osc + CombL.ar(osc, delaytime: echo * sus * 2, maxdelaytime: 2, decaytime: decay);
ReplaceOut.ar(bus, osc)}).add;