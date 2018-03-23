(
SynthDef.new(\pads,
	{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0|
		var osc, env, filter;
		freq = In.kr(bus, 1);
		freq = [freq, freq+fmod];
		amp=(amp * 2);

		freq = freq * [1, Line.kr(1.01, 1.005, sus)];

		osc = SinOsc.ar(freq + (Line.kr(10, (freq * 2), sus) * Pulse.ar(freq * rate, width: SinOsc.kr(0.225/sus))), mul:0.5);

		env = EnvGen.ar(Env([0, 0.8, 0.5, 0],[0.2 * sus, 0.5 * sus, 0.7 * sus]));

		osc = BBandPass.ar(osc, 1600, 2);

		osc = osc * env * amp;

		osc = Mix(osc) * 0.5;
		osc = Pan2.ar(osc, pan);
		ReplaceOut.ar(bus, osc)}).add;
)
