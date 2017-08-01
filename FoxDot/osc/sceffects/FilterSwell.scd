SynthDef.new(\filterSwell,
{|bus, hpr, swell, sus|
var osc,env;
osc = In.ar(bus, 2);
env = EnvGen.kr(Env([0,1,0], times:[(sus*0.125), (sus*0.25)], curve:4));
osc = RHPF.ar(osc, env * swell, hpr);
ReplaceOut.ar(bus, osc)}).add;