SynthDef.new(\creep,
{|pan=0, freq=0, sus=1, bus=0, fmod=0, rate=0, amp=1, vib=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 4);
osc=PMOsc.ar(freq, (freq * 2), 10);
env=EnvGen.ar(Env(times: [sus, 0.001],curve: 'exp',levels: [0.0001, amp, 0]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
