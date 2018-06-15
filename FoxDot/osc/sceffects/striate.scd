SynthDef.new(\striate,
{|bus, rate, striate, sus, buf|
var osc;
osc = In.kr(bus, 1);
osc = osc * LFPulse.ar(striate / sus, width:  (BufDur.kr(buf) / rate) / sus);
ReplaceOut.kr(bus, osc)}).add;