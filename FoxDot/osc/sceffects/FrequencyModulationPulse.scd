SynthDef.new(\FrequencyModulationPulse,
{|bus, fm_pulse, fm_pulse_i|
var osc;
osc = In.kr(bus, 1);
osc = osc + (fm_pulse_i * Pulse.kr(osc * fm_pulse));
ReplaceOut.kr(bus, osc)}).add;