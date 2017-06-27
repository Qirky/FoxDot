SynthDef.new(\reverb,
{|bus, verb, room|
var osc;
osc = In.ar(bus, 2);
osc = FreeVerb.ar(osc, verb, room);
ReplaceOut.ar(bus, osc)}).add;