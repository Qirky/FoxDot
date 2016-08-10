SynthDef.new( \viola,{|vib=6, vibVar=0.04, echo=0, depthVar=0.1, vibDelay=0, slide=0, delay=0, sus=1, hpf=0, pan=0, scrub=0, verb=0.33, amp=1, freq=0, buf=0, echoOn=0, room=1, rate=0, depth=0.02, grain=0, lpf=20000, slidefrom=1|var osc,env;
freq=freq;
osc=LPF.ar(HPF.ar(PMOsc.ar(freq, Vibrato.kr(freq, delay: (sus * 0.25), rate: vib, depth: 0.008), 10, mul: (amp / 2)), hpf), (lpf + 1));
env=EnvGen.ar(Env.perc((0.25 * sus), (2.5 * sus), level: amp, releaseTime: sus).delay(delay), doneAction: 2);
Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;