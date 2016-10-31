SynthDef.new(\scratch,
{|vib=0, scrub=0, echo=0, rate=0.04, verb=0.25, lpf=20000, amp=1, freq=0, buf=0, delay=0, echoOn=0, room=0.3, depth=0.5, chop=0, slide=0, grain=0, pan=0, fmod=0, sus=1, bits=24, hpf=0, slidefrom=1|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq * Crackle.ar(1.5));
osc=Decimator.ar((LPF.ar(HPF.ar(SinOsc.ar(Vibrato.kr((freq * Crackle.ar(1.5)), 2, 3, depthVariation: depth, rateVariation: rate), mul: amp), hpf), (lpf + 1)) * LFPulse.ar((chop / sus))), rate: 44100, bits: bits);
env=EnvGen.ar(Env(releaseTime: sus, level: amp, levels: [0, amp, 0], times: [(sus / 2), (sus / 2)]), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;