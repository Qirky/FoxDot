SynthDef.new(\nylon,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
osc=(LFPulse.ar(freq, 0.5, (0.33 * rate), 0.25) + LFPar.ar((freq + 0.5), 1, 0.1, 0.25));
env=EnvGen.ar(Env.perc(level: amp,curve: -4,releaseTime: (sus * 3),attackTime: 0.000125), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
