SynthDef.new(\hpf,
	{|bus=0, hpf=0|
		var osc;
		osc = In.ar(bus, 2);
		osc = HPF.ar(osc, hpf);
		Out.ar(bus, osc)}).add;

SynthDef.new(\lpf,
	{|bus=0, lpf=20000|
		var osc;
		osc = In.ar(bus, 2);
		osc = LPF.ar(osc, lpf);
		Out.ar(bus, osc)}).add;

SynthDef.new(\echo,
	{|bus=0, echo=0|
		var osc;
		osc = In.ar(bus, 2);
		osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2)));
		Out.ar(bus, osc)}).add;

SynthDef.new(\bitcrush,
	{|bus=0, bits=0|
		var osc;
		osc = In.ar(bus, 2);
		osc=Decimator.ar(osc, rate: 44100, bits: bits);
		Out.ar(bus, osc)}).add;

SynthDef.new(\reverb,
	{|bus=0, verb=0, room=0|
		var osc;
		osc = In.ar(bus, 2);
		osc=FreeVerb.ar(osc, verb, room);
		Out.ar(bus, osc)}).add;

SynthDef.new(\chop,
	{|bus=0, chop=0, sus=1|
		var osc;
		osc = In.ar(bus, 2);
		osc=(osc * LFPulse.ar((chop / sus)));
		Out.ar(bus, osc) }).add;

SynthDef.new(\makeSound,
	{ arg bus; Out.ar(0, In.ar(bus, 2);)}).add;