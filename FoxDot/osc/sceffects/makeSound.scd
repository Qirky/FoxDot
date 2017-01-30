SynthDef.new(\makeSound,
	{ arg bus, sus; var osc;
		osc = In.ar(bus, 2);
		Line.ar(dur: sus, doneAction: 14);
		DetectSilence.ar(osc, amp:0.0001, time: 0.1, doneAction: 14);
		Out.ar(0, osc)}).add;