SynthDef.new(\play2,
{|scrub=0, bus=0, rate=1, amp=1, freq=0, buf=0, cut=1, room=0.1, sus=1, fmod=0, bits=0, pan=0|
var osc, env;
Line.kr(0,1, BufDur.kr(buf) * cut * (1 / rate), doneAction: 2);
amp=(amp * 0.75);
rate=(((scrub * LFPar.kr((scrub / 4))) + rate) - scrub);
osc=PlayBuf.ar(2, buf, (BufRateScale.ir(buf) * rate), doneAction: 2);
osc=((osc * amp) * 3);
osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
	ReplaceOut.ar(bus, osc)}).add;
