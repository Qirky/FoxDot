SynthDef.new(\viola,
{|vib=6, scrub=0, echo=0, rate=1, verb=0.33, lpf=20000, amp=1, freq=0, buf=0, delay=0, echoOn=0, room=0.3, chop=0, slide=0, grain=0, pan=0, fmod=0, sus=1, bits=24, hpf=0, slidefrom=1|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=freq;
osc=Decimator.ar((LPF.ar(HPF.ar(PMOsc.ar(freq, Vibrato.kr(freq, delay: (sus * 0.25), rate: vib, depth: 0.008), 10, mul: (amp / 2)), hpf), (lpf + 1)) * LFPulse.ar((chop / sus))), rate: 44100, bits: bits);
env=EnvGen.ar(Env.perc((0.25 * sus), (2.5 * sus), level: amp, releaseTime: sus), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;