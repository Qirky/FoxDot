SynthDef.new(\vibrato,
{|bus, vib, vibdepth|
var osc;
osc = In.kr(bus, 1);
osc = Vibrato.ar(osc, vib, depth: vibdepth);
ReplaceOut.kr(bus, osc)}).add;