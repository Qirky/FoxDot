SynthDef.new(\quin,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp * 2);
osc=Klank.ar(`[[1, 2, 3, 4], [1, 4, 9, 16], [16, 9, 10, 20]], SinOsc.ar(0.5), [(freq * 0.99), freq]);
osc=LPF.ar(osc, Line.ar(4000, 40, dur: (0.25 / rate)));
env=EnvGen.ar(Env.perc(level: amp,curve: -12,attackTime: 0.01,releaseTime: 4), doneAction: 2);

osc = osc * env;
osc = Limiter.ar(osc, level: 1);
osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
	Out.ar(bus, osc)}).add;