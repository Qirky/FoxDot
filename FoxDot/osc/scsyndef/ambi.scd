(
SynthDef.new(\ambi,
	{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0|
		var osc, env, filter;
		freq = In.kr(bus, 1);
		freq = [freq, freq+fmod];
		freq = freq + ( (XLine.kr(Rand(freq/4,freq*4),freq, sus*3/4))  * SinOsc.ar(freq * (2**rate/4)));
		osc=SinOsc.ar(freq, phase:Rand(0,2)!2);
		env = EnvGen.ar(Env([0,0.5 * amp, 0.5 * amp,0],[sus/4, sus*3/4, sus/4]));
		filter = BHiPass.ar(filter, 200);
		osc = osc * env * 0.25;
		osc = Pan2.ar(osc, pan);
		ReplaceOut.ar(bus, osc)}).add;
)

