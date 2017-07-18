SynthDef.new(\startSound,
{ arg bus, rate=1, sus; var osc;
	ReplaceOut.kr(bus, rate)}).add;
