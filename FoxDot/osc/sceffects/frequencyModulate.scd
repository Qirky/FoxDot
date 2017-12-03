SynthDef.new(\frequencyModulate,
{|bus, fmod|
var osc;
osc = In.kr(bus, 1);
osc = [osc, osc+fmod];
ReplaceOut.kr(bus, osc)}).add;