(
SynthDef.new(\pads,
	{|amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0|
		var osc, env, test;
		freq = In.kr(bus, 1);
		freq = [freq, freq+fmod];
		amp=(amp * 1.5);
		freq=(freq + [0, 1]);
		osc=(SinOsc.ar(freq, mul: amp / 3) + Pulse.ar(freq + LFNoise0.ar(16, mul:2), width:0.05, mul:0.05));
		osc=HPF.ar(osc, 2000);
		env=EnvGen.ar(Env.perc(attackTime: 0.02, releaseTime: sus, level: amp, curve: \sin), doneAction: 0);
		osc=(osc * env);
		test = Klank.ar(`[[1, 2, 3, 4], [1, 1, 1, 1], [2, 2, 2, 2]], ClipNoise.ar(0.0001).dup, freq) * Line.ar(1,0, sus * 1.25);
		osc = osc + test;
		osc = Mix(osc) * 0.5;
		osc = Pan2.ar(osc, pan);
		ReplaceOut.ar(bus, osc)}).add;
)