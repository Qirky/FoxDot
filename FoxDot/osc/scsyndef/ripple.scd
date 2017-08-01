SynthDef.new(\ripple,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=(amp / 6);
osc=(Pulse.ar([(freq / 4), ((freq / 4) + 1)], 0.2, 0.25) + Pulse.ar([(freq + 2), freq], 0.5, 0.5));
osc=(osc * SinOsc.ar((rate / sus), 0, 0.5, 1));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(0.55 * sus), (0.55 * sus)]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
