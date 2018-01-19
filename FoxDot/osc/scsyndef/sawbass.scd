SynthDef(\sawbass,
	{|amp=1, sus=0.2, pan=0, bus=0, freq=440, cutoff=1000, rq=0.5, drive=2.0, fmod=0|
		var osc1, osc2, filter, filter2, env, filterenv, ab;
		amp = amp * 0.2;
		freq = (In.kr(bus) / 4) + fmod;
		osc1 = Saw.ar(freq);
		osc2 = Mix(Saw.ar(freq * [0.25,1,1.5], [0.5,0.4,0.1]));
		filterenv = EnvGen.ar(Env.adsr(0.0, 0.5, 0.2, sus), 1, doneAction: 2);
		filter =  RLPF.ar(osc1 + osc2, cutoff * filterenv + 100, rq);
		ab = abs(filter);
		filter2 = (filter * (ab + drive) / (filter ** 2 + (drive - 1) * ab + 1));
		filter2 = BLowShelf.ar(filter2, 300, 1.0, -12);
		filter2 = BPeakEQ.ar(filter2, 1600, 1.0, -6);
		//env = EnvGen.ar(Env.adsr(0.01, 0.0, sus / 2, 0.05), 1, doneAction:3);
		env = EnvGen.ar(Env([0,1,0.8,0.8,0], [0.01, 0, sus, 0.05]), doneAction:3);
		ReplaceOut.ar(bus,Pan2.ar((filter + filter2) * env * amp, pan))}).add;
