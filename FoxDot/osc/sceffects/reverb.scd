SynthDef.new(\reverb,
{|bus, room, mix|
var osc;
osc = In.ar(bus, 2);
osc = FreeVerb.ar(osc, mix, room);
ReplaceOut.ar(bus, osc)}).add;