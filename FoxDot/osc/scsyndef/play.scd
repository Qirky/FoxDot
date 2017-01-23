SynthDef.new(\play,
{|scrub=0, room=0.1, bus=0, rate=1, bitcrush=24, sus=1, fmod=0, amp=1, freq=0, buf=0, pan=0|
var osc, env;

amp=(amp * 0.75);
rate=(((scrub * LFPar.kr((scrub / 4))) + rate) - scrub);
osc=PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * rate));
osc=(((osc * EnvGen.ar(Env(levels: [(amp * 1), (amp * 1), (amp * 0)],curve: 'step',times: [(sus * 2), 0]), doneAction: 0)) * amp) * 3);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: 2), doneAction: 2);

osc = osc * env;
osc = Limiter.ar(osc, level: 1);
osc = osc * [min(1, (1-pan)/2), min(1, (pan+1)/2)];
	Out.ar(bus, osc)}).add;