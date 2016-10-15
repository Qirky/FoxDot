SynthDef.new(\fuzz,
{|vib=0, grain=0, echoOn=0, scrub=0, room=0.3, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0.25, sus=1, slidefrom=1, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 6);
freq=(freq / 2);
osc=Decimator.ar(LPF.ar(HPF.ar(LFSaw.ar(LFSaw.kr((freq / 2), 0, (freq / 2), ((freq / 2) * 2))), hpf), (lpf + 1)), rate: 44100, bits: bits);
env=EnvGen.ar(Env([0, amp, amp, 0], [0, sus, 0], releaseTime: sus, level: amp, levels: [0, amp, amp, 0], curve: 'step', times: [0, sus, 0]), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;