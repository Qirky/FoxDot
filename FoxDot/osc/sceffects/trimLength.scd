SynthDef.new(\trimLength,
{|bus, cut, sus|
var osc;
osc = In.ar(bus, 2);
osc = osc * EnvGen.ar(Env(levels: [1,1,0.01], curve: 'step', times: [sus * cut, 0.01]));
ReplaceOut.ar(bus, osc)}).add;