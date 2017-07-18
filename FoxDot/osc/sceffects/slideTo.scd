SynthDef.new(\slideTo,
{|bus, slide, sus|
var osc;
osc = In.kr(bus, 1);
osc = Line.ar(osc, osc * (slide + 1), sus);
ReplaceOut.kr(bus, osc)}).add;