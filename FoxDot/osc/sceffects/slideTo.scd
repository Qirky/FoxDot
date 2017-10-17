SynthDef.new(\slideTo,
{|bus, slide, sus, slidedelay|
var osc;
osc = In.kr(bus, 1);
osc = osc * EnvGen.ar(Env([1, 1, slide + 1], [sus*slidedelay, sus*(1-slidedelay)]));
ReplaceOut.kr(bus, osc)}).add;