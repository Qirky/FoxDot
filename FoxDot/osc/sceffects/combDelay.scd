SynthDef.new(\combDelay,
{|bus, echotime, beat_dur, echo|
var osc;
osc = In.ar(bus, 2);
osc = osc + CombL.ar(osc, delaytime: echo * beat_dur, maxdelaytime: 2 * beat_dur, decaytime: echotime * beat_dur);
ReplaceOut.ar(bus, osc)}).add;