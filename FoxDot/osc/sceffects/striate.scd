SynthDef.new(\striate,
{|bus, buf, rate, sus, striate|
var osc;
osc = In.kr(bus, 1);
osc = osc * LFPulse.ar(striate / sus, width:  (BufDur.kr(buf) / rate) / sus);
ReplaceOut.kr(bus, osc)}).add;