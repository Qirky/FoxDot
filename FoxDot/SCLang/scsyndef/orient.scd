SynthDef.new(\orient,
{|vib=0, scrub=0, echo=0, rate=1, verb=0.7, lpf=20000, amp=1, freq=0, buf=0, delay=0, echoOn=0, room=10, chop=0, slide=0, grain=0, pan=0, fmod=0, sus=1, bits=24, hpf=0, slidefrom=1|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=Decimator.ar((LPF.ar(HPF.ar((LFPulse.ar(freq, 0.5, 0.25, 0.25) + LFPulse.ar(freq, 1, 0.1, 0.25)), hpf), (lpf + 1)) * LFPulse.ar((chop / sus))), rate: 44100, bits: bits);
env=EnvGen.ar(Env.perc(level: amp, releaseTime: sus), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;