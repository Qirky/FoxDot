SynthDef.new(\striate,
{|bus, striate, sus, buf, rate|
var osc;
osc = In.kr(bus, 1);
osc = osc * LFPulse.ar(striate / sus, width:  (BufDur.kr(buf) / rate) / sus);
ReplaceOut.kr(bus, osc)}).add;