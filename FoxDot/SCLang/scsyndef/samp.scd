SynthDef.new( \samp,{|vib=0, vibVar=0.04, echo=0, depthVar=0.1, vibDelay=0, slide=0, delay=0, sus=1, hpf=0, pan=0, scrub=0, verb=0.25, amp=1, freq=0, buf=0, echoOn=0, room=0.1, rate=1, depth=0.02, grain=0, lpf=20000, slidefrom=1|var osc,env;
freq=Vibrato.kr(Line.ar((freq * slidefrom), (freq * (1 + slide)), sus), delay: vibDelay, depthVariation: depthVar, rate: vib, rateVariation: vibVar, depth: depth);
rate=(((scrub * LFPar.kr((scrub / 4))) + rate) - scrub);
osc=LPF.ar(HPF.ar(((PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * (((scrub * LFPar.kr((scrub / 4))) + rate) - scrub)), startPos: Line.kr(0, (BufFrames.kr(buf) * 0.75), (sus * 2)), trigger: LFPar.kr(grain)) * amp) * 3), hpf), (lpf + 1));
env=EnvGen.ar(Env([0, amp, amp, 0], [0, (sus * 2), 0], releaseTime: sus, level: amp, levels: [0, amp, amp, 0], times: [0, (sus * 2), 0]).delay(delay), doneAction: 2);
Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;