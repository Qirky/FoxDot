(
SynthDef.new(\ambi,
	{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0|
		var osc, env, filter;
		freq = In.kr(bus, 1);
		freq = freq + fmod;
		freq = freq + ( (XLine.kr(freq * rate, freq + LFNoise2.ar(4, mul:1), sus))  * SinOsc.ar(freq + LFNoise2.ar(4, mul:2)));
		osc=SinOsc.ar(freq + Rand(0.99,1.01), phase:Rand(0,2));
		env = EnvGen.ar(Env([0,0.5 * amp, 0.5 * amp,0],[sus/4, sus, sus/4]));
		filter = BHiPass.ar(osc, 200);
		osc = osc * env * 0.25;
		osc = Pan2.ar(osc, pan);
		ReplaceOut.ar(bus, osc)}).add;
)

