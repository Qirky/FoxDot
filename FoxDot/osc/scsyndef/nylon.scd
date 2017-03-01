SynthDef.new(\nylon,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, bits=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=(LFPulse.ar(freq, 0.5, (0.33 * rate), 0.25) + LFPar.ar((freq + 0.5), 1, 0.1, 0.25));
env=EnvGen.ar(Env.perc(level: amp,curve: -4,attackTime: 0.000125,releaseTime: (sus * 3)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
