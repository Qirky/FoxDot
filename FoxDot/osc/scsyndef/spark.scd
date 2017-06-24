SynthDef.new(\spark,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, bits=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp + 1e-05);
freq=[freq, (freq + LFNoise2.ar(50).range(-2, 2))];
osc=((LFSaw.ar((freq * 1.002), iphase: Saw.ar(0.1)) * 0.3) + (LFSaw.ar(freq, iphase: Saw.ar(0.1)) * 0.3));
osc=(((osc * Line.ar(amp, (amp / 10000), (sus * 1.5))) * 0.3) * Line.ar(0.01, 1, (sus * 0.033)));
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
