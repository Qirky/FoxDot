SynthDef.new(\spick,
{|vib=0, bus=0, slide=0, rate=1, sus=1, slidefrom=1, fmod=0, amp=1, freq=0, bits=0, pan=0|
var osc, env;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 4);
sus=(sus * 1.25);
osc=(LFPulse.ar(freq).distort + Impulse.ar((freq + 1)).tan);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.1,releaseTime: sus), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
