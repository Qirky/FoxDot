SynthDef.new(\MaskEnvelope,
{|bus, atk, decay, sus, rel, legato, gain, amp, curve=0|
	var osc;
	osc = In.ar(bus, 2);
	sus = sus * legato;
	osc = osc * EnvGen.kr(Env([0, amp, amp, 0],[atk, sus, rel], curve: \lin), levelScale:0.75, timeScale:1, doneAction: 3);
	ReplaceOut.ar(bus, osc)
}).add;
