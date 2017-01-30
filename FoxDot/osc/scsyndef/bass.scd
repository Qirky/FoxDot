SynthDef.new(\bass,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, bits=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 4);
osc=((LFTri.ar(freq, mul: amp) + VarSaw.ar(freq, width: 0.85, mul: amp)) + SinOscFB.ar(freq, mul: (amp / 2)));
env=EnvGen.ar(Env.perc(level: amp,curve: 'lin',attackTime: 0.01,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
	ReplaceOut.ar(bus, osc)}).add;
