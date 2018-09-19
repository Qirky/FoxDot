SynthDef.new(\slideFrom,
{|bus, slidedelay, sus, slidefrom|
var osc;
osc = In.kr(bus, 1);
osc = osc * EnvGen.ar(Env([slidefrom + 1, slidefrom + 1, 1], [sus*slidedelay, sus*(1-slidedelay)]));
ReplaceOut.kr(bus, osc)}).add;