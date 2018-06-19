SynthDef.new(\glass,
{|vib=0, bus=0, fmod=0, sus=1, amp=1, rate=0, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
sus=(sus * 1.5);
amp=(amp * 1.5);
freq=(freq * [1, (1 + (0.005 * rate))]);
osc=Klank.ar(`[[2, 4, 9, 16], [1, 1, 1, 1], [2, 2, 2, 2]], (PinkNoise.ar(0.0005).dup * SinOsc.ar((freq / 4), add: 1, mul: 0.5)), freq);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: (sus * 2)), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
