SynthDef.new(\scratch,
{|vib=0, bus=0, fmod=0, sus=1, amp=1, rate=0.04, depth=0.5, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 4);
freq=(freq * Crackle.ar(1.5));
osc=SinOsc.ar(Vibrato.kr(freq, 2, 3, rateVariation: rate, depthVariation: depth), mul: amp);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
