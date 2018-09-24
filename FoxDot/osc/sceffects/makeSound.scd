SynthDef.new(\makeSound,
{ arg bus, sus; var osc;
	osc = In.ar(bus, 2);
  osc = EnvGen.ar(Env([1,1,0],[sus * 8, 0.1]), doneAction: 14) * osc;
	DetectSilence.ar(osc, amp:0.0001, time: 0.1, doneAction: 14);
OffsetOut.ar(0, osc[0]);
OffsetOut.ar(1, osc[1]);
 }).add;
