SynthDef.new(\karp,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=(amp * 0.75);
osc=LFNoise0.ar((400 + (400 * rate)), amp);
osc=(osc * XLine.ar(1, 1e-06, (sus * 0.1)));
freq=((265 / (freq * 0.666)) * 0.005);
osc=CombL.ar(osc, delaytime: freq, maxdelaytime: 2);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: [sus]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
