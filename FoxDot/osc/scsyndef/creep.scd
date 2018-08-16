SynthDef.new(\creep,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, blur=1, beat_dur=1|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=(amp / 4);
osc=PMOsc.ar(freq, (freq * 2), 10);
env=EnvGen.ar(Env(times: [sus, 0.001],levels: [0.0001, amp, 0],curve: 'exp'), doneAction: 0);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
