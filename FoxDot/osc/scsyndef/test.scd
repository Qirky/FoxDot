SynthDef.new(\test,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, bits=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp * 0.1);
osc=(VarSaw.ar([freq, (freq * 1.005)], width: ((rate - 1) / 4)) + LFSaw.ar(LFNoise0.ar((rate * 20), mul: 0.5, add: (freq * Pulse.ar(((rate - 2) + 0.1), add: 1)))));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.1,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
