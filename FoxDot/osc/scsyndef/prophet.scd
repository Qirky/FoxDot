SynthDef(\prophet,
	{|bus=0 freq=440 amp=1.0 gate=1 lforate=1 lfowidth=0.5 cutoff=6000 rq=0.4 pan=0.0, sus=0.1, fmod=0|
		var lfo, pulse, filter, env;
		// Amp is way too much for foxdot
		amp = amp * 0.1;

		freq = In.kr(bus) + [0, fmod];

		lfo = LFTri.kr(lforate * [1, 1.01], Rand(0, 2.0)!2);

		pulse = Pulse.ar(freq * [1, 1.01], lfo * lfowidth + 0.5);

		filter = RLPF.ar(pulse, cutoff, rq);

		filter = BHiPass.ar(filter, 200);

		env = EnvGen.ar(Env([0,1,0.8,0.8,0], [0.01, 0, sus, sus]), doneAction:3);

		ReplaceOut.ar(bus, Pan2.ar(Mix(filter) * env * amp * 0.5, pan))}).add
