SynthDef.new(\pluck,
	{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0, bus=0|
		var osc;
		// base behaviour
		freq = freq + fmod;
		freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
		freq = Vibrato.kr(freq, rate: vib);
		amp=(amp + 1e-05);
		freq=[freq, (freq + LFNoise2.ar(50).range(-2, 2))];
		osc=((SinOsc.ar((freq * 1.002), phase: VarSaw.ar(freq, width: Line.ar(1, 0.2, 2))) * 0.3) + (SinOsc.ar(freq, phase: VarSaw.ar(freq, width: Line.ar(1, 0.2, 2))) * 0.3));
		osc=((osc * XLine.ar(amp, (amp / 10000), (sus * 4))) * 0.3);
		// envelope

		osc = Limiter.ar(osc, level: limit);
		osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
		Out.ar(bus, osc)}).add;



SynthDef.new(\chop,
	{|bus=0, chop=0, sus=1|
		var osc;
		osc = In.ar(bus, 2);
		osc=(osc * LFPulse.ar((chop / sus)));
		Out.ar(bus, osc) }).add;

SynthDef.new(\makeSound,
	{ arg bus, sus, amp;
		var osc, env;
		env = EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: (sus * 1.5)), doneAction: 2);
		osc = In.ar(bus, 2);
		osc = osc * env;
		Out.ar(0, osc)}).add;

a = Bus.audio(s, 2);

(
b = Synth.new('pluck', ['freq', 220, 'bus', 6]);
c = Synth.after(b, 'chop', ['chop', 4, 'bus', 6]);
d = Synth.after(c, \makeSound, ['bus', 6, 'sus', 1,'amp',1]);
)