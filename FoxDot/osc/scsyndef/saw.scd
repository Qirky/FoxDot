SynthDef.new(\saw,
{|pan=0, sus=1, rate=0, vib=0, fmod=0, freq=0, amp=1, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 8);
osc=Saw.ar(freq);
osc=(osc * amp);
env=EnvGen.ar(Env(levels: [0, 1, 1, 0],curve: 'lin',times: [0.01, (sus - 0.01), 0.01]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
