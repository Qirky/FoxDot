SynthDef.new(\play1,
{|vib=0, scrub=0, bus=0, rate=1, amp=1, freq=0, buf=0, cut=1, room=0.1, slide=0, sus=1, slidefrom=1, fmod=0, bits=0, pan=0|
var osc, env;

rate=(Line.ar(rate, (rate * (1 + slide)), (sus / 2)) + 0.0001);
rate=Vibrato.kr(rate, rate: vib, depth: 0.05);
osc=PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * rate));
osc=(osc * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
