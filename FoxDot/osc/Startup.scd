Routine.run {
                	s.options.blockSize = 128;
                        s.options.memSize = 131072;
                        s.bootSync();
OSCFunc(
	{
		arg msg, time, addr, port;
		var fn, load;

		// Get local filename

		fn = msg[1].asString;

		// Add SynthDef to file

		f = File(fn, "r");
		f.readAllString.interpret;
		f.close;

	},
	'foxdot'
);

Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/exclamation/0.wav", bufnum:46);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/hash/0.wav", bufnum:48);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/percent/0.wav", bufnum:49);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/dollar/0.wav", bufnum:50);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/plus/0.wav", bufnum:51);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/asterix/0.wav", bufnum:52);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/hyphen/0.wav", bufnum:53);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/forwardslash/0.wav", bufnum:54);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/colon/0.wav", bufnum:59);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/equals/0.wav", bufnum:60);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/lessthan/0.wav", bufnum:55);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/question/0.wav", bufnum:62);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/greaterthan/0.wav", bufnum:56);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/a/upper/0.wav", bufnum:2);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/at/0.wav", bufnum:47);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/c/upper/0.wav", bufnum:5);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/b/upper/0.wav", bufnum:4);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/e/upper/0.wav", bufnum:9);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/d/upper/0.wav", bufnum:7);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/f/upper/0.wav", bufnum:11);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/i/upper/0.wav", bufnum:16);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/h/upper/0.wav", bufnum:14);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/j/upper/0.wav", bufnum:18);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/o/upper/0.wav", bufnum:23);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/q/upper/0.wav", bufnum:27);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/p/upper/0.wav", bufnum:25);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/s/upper/0.wav", bufnum:30);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/t/upper/0.wav", bufnum:32);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/w/upper/0.wav", bufnum:36);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/v/upper/0.wav", bufnum:34);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/y/upper/0.wav", bufnum:43);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/x/upper/bd1_up.wav", bufnum:41);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/x/upper/bd0_up.wav", bufnum:40);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/z/upper/0.wav", bufnum:45);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/backslash/0.wav", bufnum:58);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/caret/0.wav", bufnum:63);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/a/lower/0.wav", bufnum:1);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/b/lower/0.wav", bufnum:3);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/e/lower/0.wav", bufnum:8);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/d/lower/0.wav", bufnum:6);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/g/lower/0.wav", bufnum:12);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/f/lower/0.wav", bufnum:10);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/i/lower/0.wav", bufnum:15);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/h/lower/0.wav", bufnum:13);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/k/lower/0.wav", bufnum:19);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/j/lower/0.wav", bufnum:17);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/m/lower/0.wav", bufnum:20);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/o/lower/0.wav", bufnum:22);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/n/lower/0.wav", bufnum:21);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/q/lower/0.wav", bufnum:26);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/p/lower/0.wav", bufnum:24);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/s/lower/0.wav", bufnum:29);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/r/lower/0.wav", bufnum:28);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/t/lower/0.wav", bufnum:31);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/w/lower/0.wav", bufnum:35);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/v/lower/0.wav", bufnum:33);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/y/lower/0.wav", bufnum:42);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/x/lower/bd0.wav", bufnum:37);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/x/lower/bd1.wav", bufnum:38);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/x/lower/bd2.wav", bufnum:39);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/z/lower/0.wav", bufnum:44);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/bar/0.wav", bufnum:61);
Buffer.read(s, "C:/Users/Ryan/Documents/GitHub/FoxDot/FoxDot/snd/_/tilde/0.wav", bufnum:57);

SynthDef.new(\bass,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 4);
osc=((LFTri.ar(freq, mul: amp) + VarSaw.ar(freq, width: 0.85, mul: amp)) + SinOscFB.ar(freq, mul: (amp / 2)));
env=EnvGen.ar(Env.perc(level: amp,curve: 'lin',attackTime: 0.01,releaseTime: sus), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\bell,
{|vib=0, chop=0, echoOn=0, room=0.5, limit=1, echo=0, delay=0, rate=1, verb=0.5, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp * 4);
sus=2.5;
osc=Klank.ar(`[[0.501, 1, 0.7, 2.002, 3, 9.6, 2.49, 11, 2.571, 3.05, 6.242, 12.49, 13, 16, 24], [0.002, 0.02, 0.001, 0.008, 0.02, 0.004, 0.02, 0.04, 0.02, 0.005, 0.05, 0.05, 0.02, 0.03, 0.04], [1.2, 1.2, 1.2, 0.9, 0.9, 0.9, 0.25, 0.25, 0.25, 0.14, 0.14, 0.14, 0.07, 0.07, 0.07]], Impulse.ar(0.25), freq, 0, 3);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: [sus]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\blip,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp + 1e-05);
freq=[freq, (freq + LFNoise2.ar(50).range(-2, 2))];
osc=((LFCub.ar((freq * 1.002), iphase: 1.5) + (LFTri.ar(freq, iphase: Line.ar(2, 0, 0, 2)) * 0.3)) * Blip.ar((freq / 2), rate));
osc=((osc * XLine.ar(amp, (amp / 10000), (sus * 2))) * 0.3);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: (sus * 2.5)), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\bug,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 5);
osc=(Pulse.ar([freq, (freq * 1.0001)], width: [0.09, 0.16, 0.25]) * SinOsc.ar((rate * 4)));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: (sus * 1.5),releaseTime: sus), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\charm,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=(SinOsc.ar([freq, (freq + 4)], mul: (amp / 4)) + VarSaw.ar((freq * 8), 10, mul: (amp / 8)));
osc=LPF.ar(osc, SinOsc.ar(Line.ar(1, (rate * 4), (sus / 8)), 0, (freq * 2), ((freq * 2) + 10)));
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
SynthDef.new(\creep,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 4);
osc=PMOsc.ar(freq, (freq * 2), 10);
env=EnvGen.ar(Env(levels: [0, amp],curve: 'exp',times: [sus, 0.001]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\crunch,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp * 0.5);
osc=LFNoise0.ar(((Crackle.kr(1.95) * freq) * 15), mul: amp);
env=EnvGen.ar(Env.perc(level: (amp / 4),curve: 0,attackTime: 0.01,releaseTime: 0.1), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\dab,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=(HPF.ar(Saw.ar((freq / 4), mul: (amp / 2)), 2000) + VarSaw.ar((freq / 4), mul: amp, width: EnvGen.ar(Env.perc(level: 0.5,curve: -5,attackTime: (sus / 20),releaseTime: (sus / 4)), doneAction: 0)));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus * 0.25), (sus * 1)]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\dirt,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 4);
osc=((LFSaw.ar(freq, mul: amp) + VarSaw.ar((freq + 1), width: 0.85, mul: amp)) + SinOscFB.ar((freq - 1), mul: (amp / 2)));
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
SynthDef.new(\dub,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 4);
amp=(amp * 2);
osc=(LFTri.ar(freq, mul: amp) + SinOscFB.ar(freq, mul: amp));
env=EnvGen.ar(Env.sine(dur: sus,level: amp), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\fuzz,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq / 2);
amp=(amp / 6);
osc=LFSaw.ar(LFSaw.kr(freq, 0, freq, (freq * 2)));
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: [sus]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\growl,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
sus=(sus * 1.5);
osc=(SinOsc.ar((freq + SinOsc.kr(0.5, mul: 2, add: 1)), mul: amp) * Saw.ar(((sus / 1.5) * 32)));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\klank,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
sus=(sus * 1.5);
osc=Klank.ar(`[[1, 2, 3, 4], [1, 1, 1, 1], [2, 2, 2, 2]], ClipNoise.ar(0.0005).dup, freq);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\marimba,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=Klank.ar(`[[0.5, 1, 4, 9], [0.5, 1, 1, 1], [1, 1, 1, 1]], PinkNoise.ar([0.007, 0.007]), [freq, freq], [0, 2]);
sus=1;
env=EnvGen.ar(Env.perc(level: amp,curve: -6,attackTime: 0.001,releaseTime: sus), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\noise,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=LFNoise0.ar(freq, amp);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\orient,
{|vib=0, chop=0, echoOn=0, room=10, limit=1, echo=0, delay=0, rate=1, verb=0.7, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=(LFPulse.ar(freq, 0.5, 0.25, 0.25) + LFPulse.ar(freq, 1, 0.1, 0.25));
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
SynthDef.new(\pads,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 2);
osc=SinOsc.ar([freq, (freq + 2)], mul: amp);
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
SynthDef.new(\play,
{|chop=0, echoOn=0, scrub=0, room=0.1, bitcrush=24, buf=0, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, fmod=0, lpf=20000, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
rate=(((scrub * LFPar.kr((scrub / 4))) + rate) - scrub);
osc=PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * rate));
osc=(((osc * EnvGen.ar(Env(levels: [(amp * 1), (amp * 1), (amp * 0)],curve: 'step',times: [(sus * 2), 0]), doneAction: 0)) * amp) * 3);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: 2), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\pluck,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp + 1e-05);
freq=[freq, (freq + LFNoise2.ar(50).range(-2, 2))];
osc=((SinOsc.ar((freq * 1.002), phase: VarSaw.ar(freq, width: Line.ar(1, 0.2, 2))) * 0.3) + (SinOsc.ar(freq, phase: VarSaw.ar(freq, width: Line.ar(1, 0.2, 2))) * 0.3));
osc=((osc * XLine.ar(amp, (amp / 10000), (sus * 4))) * 0.3);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: (sus * 1.5)), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\pulse,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 4);
osc=Pulse.ar(freq);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: [sus]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\quin,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp * 2);
osc=Klank.ar(`[[1, 2, 3, 4], [1, 4, 9, 16], [16, 9, 10, 20]], SinOsc.ar(0.5), [(freq * 0.99), freq]);
osc=LPF.ar(osc, Line.ar(4000, 40, dur: (0.25 / rate)));
env=EnvGen.ar(Env.perc(level: amp,curve: -12,attackTime: 0.01,releaseTime: 4), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\rave,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=Gendy1.ar((rate - 1), mul: (amp / 2), minfreq: freq, maxfreq: (freq * 2));
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
SynthDef.new(\ripple,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 6);
osc=(Pulse.ar([(freq / 4), ((freq / 4) + 1)], 0.2, 0.25) + Pulse.ar([(freq + 2), freq], 0.5, 0.5));
osc=(osc * SinOsc.ar((rate / sus), 0, 0.5, 1));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [0.55, 0.55]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\saw,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 4);
osc=Saw.ar(freq);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: [sus]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\scatter,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
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

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\scratch,
{|vib=0, chop=0, echoOn=0, room=0.3, depth=0.5, limit=1, echo=0, delay=0, rate=0.04, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
freq=(freq * Crackle.ar(1.5));
osc=SinOsc.ar(Vibrato.kr(freq, 2, 3, depthVariation: depth, rateVariation: rate), mul: amp);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\snick,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=(LFPar.ar(freq, mul: 1) * Blip.ar(((rate + 1) * 4)));
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
SynthDef.new(\soprano,
{|vib=5, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.5, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 2);
osc=(SinOsc.ar((freq * 3), mul: amp) + SinOscFB.ar((freq * 3), mul: (amp / 2)));
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\spark,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp + 1e-05);
verb=(verb + 0.1);
freq=[freq, (freq + LFNoise2.ar(50).range(-2, 2))];
osc=((LFSaw.ar((freq * 1.002), iphase: Saw.ar(0.1)) * 0.3) + (LFSaw.ar(freq, iphase: Saw.ar(0.1)) * 0.3));
osc=((osc * Line.ar(amp, (amp / 10000), (sus * 1.5))) * 0.3);
env=EnvGen.ar(Env(levels: [(amp * 1), (amp * 1)],curve: 'step',times: (sus * 2)), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
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
SynthDef.new(\varsaw,
{|vib=0, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.25, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=VarSaw.ar([freq, (freq * 1.005)], mul: (amp / 4), width: rate);
env=EnvGen.ar(Env(levels: [0, amp, 0],curve: 'lin',times: [(sus / 2), (sus / 2)]), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\viola,
{|vib=6, chop=0, echoOn=0, room=0.3, limit=1, echo=0, delay=0, rate=1, verb=0.33, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
osc=PMOsc.ar(freq, Vibrato.kr(freq, delay: (sus * 0.25), rate: vib, depth: 0.008), 10, mul: (amp / 2));
env=EnvGen.ar(Env.perc(level: amp,curve: 0,attackTime: (0.25 * sus),releaseTime: (0.75 * sus)), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
SynthDef.new(\zap,
{|vib=0, chop=0, echoOn=0, room=0, limit=1, echo=0, delay=0, rate=1, verb=0, sus=1, slide=0, fmod=0, lpf=20000, slidefrom=1, amp=1, freq=0, bits=24, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 10);
osc=(Saw.ar(((freq * [1, 1.01]) + LFNoise2.ar(50).range(-2, 2))) + VarSaw.ar((freq + LFNoise2.ar(50).range(-2, 2)), 1));
env=EnvGen.ar(Env.perc(level: amp,curve: -10,attackTime: 0.025,releaseTime: sus), doneAction: 2);
osc=HPF.ar(osc, hpf);
osc=LPF.ar(osc, (lpf + 1));
osc=(osc * LFPulse.ar((chop / sus)));
osc=(osc + (CombL.ar(osc, delaytime: echo, maxdelaytime: 2) * echoOn));
osc=Decimator.ar(osc, rate: 44100, bits: bits);

osc = osc * env;
osc = Limiter.ar(osc, level: limit);
osc = Pan2.ar(FreeVerb.ar(osc, verb, room), pan);
	Out.ar(0, osc)}).add;
};