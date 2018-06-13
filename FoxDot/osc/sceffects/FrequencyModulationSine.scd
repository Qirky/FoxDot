SynthDef.new(\FrequencyModulationSine,
{|bus, fm_sin_i, fm_sin|
var osc;
osc = In.kr(bus, 1);
osc = osc + (fm_sin_i * SinOsc.kr(osc * fm_sin));
ReplaceOut.kr(bus, osc)}).add;