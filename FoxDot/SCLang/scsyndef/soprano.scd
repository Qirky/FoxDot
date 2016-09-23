SynthDef.new(\soprano,
{|vib=5, grain=0, echoOn=0, scrub=0, room=0.3, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0.5, sus=1, slidefrom=1, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 2);
osc=LPF.ar(HPF.ar((SinOsc.ar((freq * 3), mul: (amp / 2)) + SinOscFB.ar((freq * 3), mul: ((amp / 2) / 2))), hpf), (lpf + 1));
env=EnvGen.ar(Env(releaseTime: sus, level: amp, levels: [0, amp, 0], times: [(sus / 2), (sus / 2)]), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;