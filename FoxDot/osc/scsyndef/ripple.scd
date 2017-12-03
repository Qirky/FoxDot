SynthDef.new(\ripple,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 6);
osc=(Pulse.ar([(freq / 4), ((freq / 4) + 1)], 0.2, 0.25) + Pulse.ar([(freq + 2), freq], 0.5, 0.5));
osc=(osc * SinOsc.ar((rate / sus), 0, 0.5, 1));
env=EnvGen.ar(Env(times: [(0.55 * sus), (0.55 * sus)],levels: [0, amp, 0],curve: 'lin'), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
