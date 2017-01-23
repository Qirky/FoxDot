SynthDef.new(\viola,
{|vib=6, bus=0, slide=0, rate=1, verb=0.33, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=PMOsc.ar(freq, Vibrato.kr(freq, delay: (sus * 0.25), rate: vib, depth: 0.008), 10, mul: (amp / 2));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: (0.25 * sus),releaseTime: (0.75 * sus)), doneAction: 2);

osc = osc * env;
osc = Limiter.ar(osc, level: 1);
osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
	Out.ar(bus, osc)}).add;