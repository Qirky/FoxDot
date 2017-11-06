SynthDef.new(\star,
{|vib=0, rate=0, sus=1, fmod=0, bus=0, amp=1, freq=0, pan=0|
var osc, env;
freq = In.kr(bus, 1);
freq = freq + fmod;
amp=((amp * 2) + 1e-05);
freq=[(freq / 2), ((freq / 2) + LFNoise2.ar(50).range(-2, 2))];
osc=((Saw.ar((freq * 1.002), phase: VarSaw.ar(freq, width: Line.ar(1, 0.2, sus))) * 0.3) + (Saw.ar((freq + 2), phase: VarSaw.ar((freq + 2), width: Line.ar(1, 0.2, sus))) * 0.3));
osc=((osc * XLine.ar(amp, (amp / 10000), (sus * 3), doneAction: 2)) * Line.ar(0.01, 0.5, (sus / 6)));
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
