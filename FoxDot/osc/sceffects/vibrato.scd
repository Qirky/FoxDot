SynthDef.new(\vibrato,
{|bus, vibdepth, vib|
var osc;
osc = In.kr(bus, 1);
osc = Vibrato.ar(osc, vib, depth: vibdepth);
ReplaceOut.kr(bus, osc)}).add;