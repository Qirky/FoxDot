SynthDef.new(\bandPassFilter,
{|bus, bpnoise, bpf, bpr, sus|
var osc;
osc = In.ar(bus, 2);
bpnoise = bpnoise / sus;
bpf = LFNoise1.kr(bpnoise).exprange(bpf * 0.5, bpf * 2);
bpr = LFNoise1.kr(bpnoise).exprange(bpr * 0.5, bpr * 2);
osc = BPF.ar(osc, bpf, bpr);
ReplaceOut.ar(bus, osc)}).add;