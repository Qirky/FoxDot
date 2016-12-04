SynthDef.new( \rev,{|vib=0, vibVar=0.04, echo=0, depthVar=0.1, vibDelay=0, slide=0, delay=0, sus=1, hpf=0, pan=0, scrub=0, verb=0.25, amp=1, freq=0, buf=0, echoOn=0, room=1, rate=0, depth=0.02, grain=0, lpf=20000, slidefrom=1|var osc,env;
amp=(amp / 4);
freq=Vibrato.kr(Line.ar((freq * slidefrom), (freq * (1 + slide)), sus), delay: vibDelay, depthVariation: depthVar, rate: vib, rateVariation: vibVar, depth: depth);
osc=LPF.ar(HPF.ar(PMOsc.ar(Vibrato.kr(Line.ar((freq * slidefrom), (freq * (1 + slide)), sus), delay: vibDelay, depthVariation: depthVar, rate: vib, rateVariation: vibVar, depth: depth), (Vibrato.kr(Line.ar((freq * slidefrom), (freq * (1 + slide)), sus), delay: vibDelay, depthVariation: depthVar, rate: vib, rateVariation: vibVar, depth: depth) * 2), 10), hpf), (lpf + 1));
env=EnvGen.ar(Env(releaseTime: sus, level: amp, levels: [0.001, amp, 0.001], curve: 'exp', times: [sus, 0.001]).delay(delay), doneAction: 2);
Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;