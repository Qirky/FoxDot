SynthDef.new(\glissando,
{|bus, glide, glide_delay, sus|
var osc;
osc = In.kr(bus, 1);
osc = osc * EnvGen.ar(Env([1, 1, (1.059463**glide)], [sus*glide_delay, sus*(1-glide_delay)]));
ReplaceOut.kr(bus, osc)}).add;