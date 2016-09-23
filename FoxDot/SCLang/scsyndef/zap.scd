SynthDef.new(\zap,
{|vib=0, grain=0, echoOn=0, scrub=0, room=0, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0, sus=1, slidefrom=1, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 10);
osc=LPF.ar(HPF.ar((Saw.ar(((freq * [1, 1.01]) + LFNoise2.ar(50).range(-2, 2))) + VarSaw.ar((freq + LFNoise2.ar(50).range(-2, 2)), 1)), hpf), (lpf + 1));
env=EnvGen.ar(Env.perc(attackTime: 0.025, level: amp, curve: -10, releaseTime: sus), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;