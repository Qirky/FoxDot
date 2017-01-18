SynthDef.new(\twang,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 2);
osc=LPF.ar(Impulse.ar([freq, (freq + 1)]), 4000);
osc=CombL.ar(osc, delaytime: [0.004, 0.003], maxdelaytime: 2);
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: 0.01,releaseTime: sus), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;