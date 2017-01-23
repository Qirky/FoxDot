SynthDef.new(\noise,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=LFNoise0.ar(freq, amp);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 2);

osc = osc * env;
osc = Limiter.ar(osc, level: 1);
osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
	Out.ar(bus, osc)}).add;