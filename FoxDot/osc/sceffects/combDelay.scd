SynthDef.new(\combDelay,
{|bus, echo, decay, beat_dur|
var osc;
osc = In.ar(bus, 2);
osc = osc + CombL.ar(osc, delaytime: echo * beat_dur, maxdelaytime: 2, decaytime: decay * beat_dur);
ReplaceOut.ar(bus, osc)}).add;