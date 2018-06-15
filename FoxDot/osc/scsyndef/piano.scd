SynthDef.new(\piano,
{|amp=1, freq=0, pan=0, rate=0, vib=0, sus=1, fmod=0, bus=0|
var osc, env;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp * 0.7);
osc=MdaPiano.ar((freq[0]), vel: (40 + (amp * 60)), decay: (sus / 4));
env=EnvGen.ar(Env(times: [sus],curve: 'step',levels: [(amp * 1), (amp * 1)]), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
