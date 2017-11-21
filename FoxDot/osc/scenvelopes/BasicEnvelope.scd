SynthDef.new(\BasicEnvelope,
{|bus, atk, decay, sus, rel, legato, gain, amp, curve=0|
	var osc;
	osc = In.ar(bus, 2);
	sus = sus * legato;
	osc = osc * EnvGen.kr(Env([0, amp, amp*gain, amp*gain, 0],[atk, decay, sus, rel * sus], curve: curve), levelScale:0.75, timeScale:1, doneAction: 3);
	ReplaceOut.ar(bus, osc)
}).add;
