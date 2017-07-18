SynthDef.new(\slideFrom,
{|bus, sus, slidefrom|
var osc;
osc = In.kr(bus, 1);
osc = Line.ar(osc * slidefrom, osc, sus);
ReplaceOut.kr(bus, osc)}).add;