(
SynthDef.new(\keys,
	{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, cutoff=400|

		var osc, env;

		freq = In.kr(bus, 1);
		freq = [freq, freq+fmod];
		freq = freq * [1, 1.005];

		amp = amp / 4;

		osc = SinOsc.ar(freq + (rate * 100) * XFade2.ar(LFPar.ar(freq * (1/2)), LFTri.ar(freq * 1)), phase: 0.2, mul: 0.8);

		osc = RHPF.ar(osc, 400, 3);

		env = EnvGen.ar(Env([0, 1, 0.9, 0.5, 0],[0.01, 0, 0.5 * sus, 1 * sus]));

		osc = Mix(osc) * env * amp;

		osc = Pan2.ar(osc, pan);
		ReplaceOut.ar(bus, osc)}).add;
)

