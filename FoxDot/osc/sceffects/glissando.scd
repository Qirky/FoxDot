SynthDef.new(\glissando,
{|bus, glide, glidedelay, sus|
var osc;
osc = In.kr(bus, 1);
osc = osc * EnvGen.ar(Env([1, 1, (1.059463**glide)], [sus*glidedelay, sus*(1-glidedelay)]));
ReplaceOut.kr(bus, osc)}).add;