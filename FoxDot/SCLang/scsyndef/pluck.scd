SynthDef.new(\pluck,
{|vib=0, grain=0, echoOn=0, scrub=0, room=0.3, chop=0, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0.25, sus=1, slidefrom=1, fmod=0, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp + 1e-05);
freq=[freq, (freq + LFNoise2.ar(50).range(-2, 2))];
osc=Decimator.ar((LPF.ar(HPF.ar(((((SinOsc.ar((freq * 1.002), phase: VarSaw.ar(freq, width: Line.ar(1, 0.2, 2))) * 0.3) + (SinOsc.ar(freq, phase: VarSaw.ar(freq, width: Line.ar(1, 0.2, 2))) * 0.3)) * XLine.ar((amp + 1e-05), ((amp + 1e-05) / 10000), (sus * 4))) * 0.3), hpf), (lpf + 1)) * LFPulse.ar((chop / sus))), rate: 44100, bits: bits);
env=EnvGen.ar(Env([0, amp, amp, 0], [0, (sus * 1.5), 0], releaseTime: sus, level: amp, levels: [0, amp, amp, 0], curve: 'step', times: [0, (sus * 1.5), 0]), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;