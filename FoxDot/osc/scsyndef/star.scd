SynthDef.new(\star,
{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, blur=1, beat_dur=1, atk=0.01, decay=0.01, rel=0.01, peak=1, level=0.8|
var osc, env;
sus = sus * blur;
freq = In.kr(bus, 1);
freq = [freq, freq+fmod];
amp=((amp * 2) + 1e-05);
freq=(freq / 2);
osc=((LFSaw.ar((freq * 1.002), iphase: VarSaw.kr(freq, width: Line.kr(1, 0.2, sus))) * 0.3) + (LFSaw.ar(((freq + LFNoise2.ar(50).range(-2, 2)) + 2), iphase: VarSaw.kr((freq + 2), width: Line.kr(1, 0.2, sus))) * 0.3));
osc=((osc * XLine.ar(amp, (amp / 10000), (sus * 3), doneAction: 2)) * Line.ar(0.01, 0.5, 0.07));
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
