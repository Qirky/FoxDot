(SynthDef.new(\scatter,
{|vib=0, grain=0, echoOn=0, scrub=0, room=0.3, chop=0, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0.25, sus=1, slidefrom=1, fmod=0, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=((Saw.ar(freq, mul: (amp / 8)) + VarSaw.ar([(freq + 2), (freq + 1)], mul: (amp / 8))) * LFNoise0.ar(rate));
env=EnvGen.ar(Env.linen(level: (sus / 2),curve: 0,attackTime: 0.01,releaseTime: (sus / 2)), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;)