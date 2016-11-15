(SynthDef.new(\play,
{|vib=0, scrub=0, bitcrush=24, echo=0, rate=1, verb=0.25, lpf=20000, amp=1, freq=0, buf=0, delay=0, echoOn=0, room=0.1, chop=0, slide=0, grain=0, pan=0, fmod=0, sus=1, bits=24, hpf=0, slidefrom=1|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
rate=(((scrub * LFPar.kr((scrub / 4))) + rate) - scrub);
osc=PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * rate));
osc=(((osc * EnvGen.ar(Env(levels: [(amp * 1), (amp * 1), (amp * 0)],curve: 'step',times: [(sus * 2), 0]), doneAction: 0)) * amp) * 3);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: 2), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;)