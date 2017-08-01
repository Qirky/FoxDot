SynthDef.new(\creep,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=(amp / 4);
osc=PMOsc.ar(freq, (freq * 2), 10);
env=EnvGen.ar(Env(levels: [0.0001, amp, 0],curve: 'exp',times: [sus, 0.001]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
