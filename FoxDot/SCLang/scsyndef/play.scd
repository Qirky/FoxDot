SynthDef.new(\play,
{|vib=0, scrub=0, echo=0, rate=1, verb=0.25, lpf=20000, amp=1, freq=0, buf=0, echoOn=0, room=0.1, delay=0, slide=0, grain=0, pan=0, bitcrush=24, sus=1, bits=24, hpf=0, slidefrom=1|
var osc, env;
amp = amp / 2;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
rate=(((scrub * LFPar.kr((scrub / 4))) + rate) - scrub);
osc=Decimator.ar(LPF.ar(HPF.ar(((PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * (((scrub * LFPar.kr((scrub / 4))) + rate) - scrub))) * amp) * 3), hpf), (lpf + 1)), rate: 44100, bits: bits);
env=EnvGen.ar(Env([0, amp, amp, 0], [0, (sus * 2), 0], releaseTime: sus, level: amp, levels: [0, amp, amp, 0], times: [0, (sus * 2), 0]), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;