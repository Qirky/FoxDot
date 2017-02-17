SynthDef.new(\play2,
{|scrub=0, bus=0, rate=1, amp=1, freq=0, buf=0, cut=1, room=0.1, sus=1, fmod=0, bits=0, pan=0|
var osc, env;
Line.kr(0,1, BufDur.kr(buf) * cut * (1 / rate), doneAction: 2);
rate=(((scrub * LFPar.kr((scrub / 4))) + rate) - scrub);
osc=PlayBuf.ar(2, buf, (BufRateScale.ir(buf) * rate), doneAction: 2);
osc=(osc * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
