SynthDef.new(\crunch,
{|vib=0, grain=0, echoOn=0, scrub=0, room=0.3, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0.25, sus=1, slidefrom=1, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp * 0.5);
osc=LPF.ar(HPF.ar(LFNoise0.ar(((Crackle.kr(1.95) * freq) * 15), mul: (amp * 0.5)), hpf), (lpf + 1));
env=EnvGen.ar(Env.perc(0.01, 0.1, ((amp * 0.5) / 4), level: amp, releaseTime: sus), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;