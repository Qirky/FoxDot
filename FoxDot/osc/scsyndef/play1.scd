SynthDef.new(\play1,
{|vib=0, scrub=0, bus=0, rate=1, amp=1, freq=0, buf=0, cut=1, room=0.1, slide=0, sus=1, coarse=0, fmod=0, slidefrom=1, bits=0, pan=0|
var osc, env;

rate=Line.ar(rate, (rate * (1 + slide)), BufDur.kr(buf), doneAction: 14);
rate=(Vibrato.kr(rate, rate: vib, depth: 0.05) * LFPulse.ar((coarse / sus)));
osc=PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * rate));
osc=(osc * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
