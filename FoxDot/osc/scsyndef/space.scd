(
SynthDef.new(\space,
	{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, rq=0.5|
		var osc, env, filter;
		freq = In.kr(bus, 1);
		freq = [freq, freq+fmod];
		amp=(amp * 2);

		freq = freq * [1, 1.01];

		osc = Ringz.ar(ClipNoise.ar(0.001).dup / 2 + Impulse.ar(0.01, mul:0.02 * rate,), freq * 3);

		osc = RHPF.ar(osc, freq * 2.5, rq);

		env = EnvGen.ar(Env([1, 0.8, 0.5, 0],[0.2 * sus, 0.5 * sus, 0.7 * sus]));

		osc = Mix(osc) * env * amp;
		osc = Pan2.ar(osc, pan);
		ReplaceOut.ar(bus, osc)}).add;
)