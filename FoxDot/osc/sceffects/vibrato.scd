SynthDef.new(\vibrato,
{|bus, vib, rate|
var osc;
osc = In.ar(bus, 2);
osc = Vibrato.ar(A2K.kr(rate), vib, depth: 0.05);
ReplaceOut.ar(bus, osc)}).add;