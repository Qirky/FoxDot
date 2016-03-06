(
// Create sample player synth

SynthDef.new( \sample_player,
	{
		arg buf=0,amp=1,pan=0,rate=1, sus=1, verb=0.2, gain=0, slow=1, scrub=0, lpf=0, grain=0;
		var sound;

		rate = (scrub * LFPar.kr(scrub / 4)) + rate - scrub;

		amp = amp * Blip.ar(2 ** grain, 0, 0.5, 0.5);

		sound = FreeVerb.ar( PlayBuf.ar(1, buf, BufRateScale.ir(buf) * rate) * amp * 2 , verb, 0.1);

		sound = sound * EnvGen.ar(Env([0,1,1,0],[0 ,sus * 2, 0]), doneAction:2);

		sound = sound + (Saw.ar(0, sound * 0.05 * gain) * (gain/100));

		sound = LPF.ar(sound, 10000 / (1 + lpf**2));

		Out.ar(0,Pan2.ar( sound, pan));
		} ).add;


SynthDef.new( \words,
	{
		arg pos=0,amp=1,pan=0,rate=1;
		var buf;
		buf = 50 + pos;
		Out.ar(0,Pan2.ar( PlayBuf.ar(1, buf, BufRateScale.ir(buf) * rate, doneAction:2) * amp * 2 , pan));
		} ).writeDefFile;


// Create synthdef with musical input

SynthDef.new( \crunch,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		osc = LFNoise0.ar(Crackle.kr(1.95) * freq * 15, mul: amp);

		env = EnvGen.ar(Env.perc(0.01,0.1,amp / 2), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \rave,
	{
		arg amp=0,sus=1,pan=0,freq=0,rate=1;

		var osc, env;

		osc = Gendy1.ar(rate-1, mul:amp/2, minfreq:freq, maxfreq:freq*2);

		env = EnvGen.ar(Env.perc(0.01, sus), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
} ).writeDefFile;


SynthDef.new( \pads,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		osc = SinOsc.ar(freq, mul:amp / 2) + SinOsc.ar(freq + 2, mul:amp / 8);

		env = EnvGen.ar(Env.perc(0.01, sus), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
} ).writeDefFile;

SynthDef.new( \banjo,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		osc = Formant.ar(freq, mul:amp/2) + LFSaw.ar(freq, mul:amp/25);

		env = EnvGen.ar(Env.perc(0.01, sus), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
} ).writeDefFile;

SynthDef.new( \charm,
	{
		arg amp=0,sus=1,pan=0,freq=0, delay=0, rate=1;

		var osc, env;

		osc = SinOsc.ar([freq, freq + 2 *2], mul:amp / 4) + VarSaw.ar(freq * 8, 10, mul:amp/8);

		osc = LPF.ar(osc, SinOsc.ar(Line.ar(1,rate*4, sus/8),0,freq*2,freq*2 + 10 ));

		env = EnvGen.ar(Env.perc(0.01, sus).delay(delay), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
} ).writeDefFile;


SynthDef.new( \bell,
	{
		|freq=465, strength=1, decay=3, sus=1,amp=1,verb=0.33,pan=0|
		var son;
		son = Klank.ar(`[
			// frequency ratios
			[0.501, 1, 0.7,   2.002, 3, 9.6,   2.49, 11, 2.571,  3.05, 6.242, 12.49, 13, 16, 24],
			// amps
			[0.002,0.02,0.001, 0.008,0.02,0.004, 0.02,0.04,0.02, 0.005,0.05,0.05, 0.02, 0.03, 0.04],
			// ring times - "stutter" duplicates each entry threefold
			[1.2, 0.9, 0.25, 0.14, 0.07].stutter(3)
			]
			, Impulse.ar(0.25), freq, 0, decay);

		son = son * EnvGen.ar(Env([0,1,1,0],[0, 2, 0]), doneAction:2) * amp * 8;

		son = FreeVerb.ar(son, verb);

		Out.ar(0, Pan2.ar(son, pan));
}).writeDefFile;

SynthDef.new( \soprano,
	{
		arg amp=0,sus=1,pan=0,freq=0,verb=0.5,freq1=0;

		var osc, env, vib;

		if ( (freq1 != 0), { freq1 = freq; }, { freq1 = freq1});

		vib = Vibrato.kr(Line.kr(freq1, freq, sus), rate:5);

		osc = SinOsc.ar(vib, mul:amp / 2) + SinOscFB.ar(vib, mul:amp / 4);

		env = EnvGen.ar(Env([0,amp / 2,0],[sus / 2, sus / 2]), doneAction:2);

		Out.ar(0,Pan2.ar( FreeVerb.ar(osc * env, verb) , pan));
		} ).writeDefFile;

SynthDef.new( \bass,
	{
		arg amp=0,sus=1,pan=0,freq=0, dist=0, verb=0.25;

		var osc, env;

		freq = freq / 4;

		amp = amp / 3;

		osc = LFTri.ar(freq, mul:amp) + VarSaw.ar(freq, width:0.85, mul: amp) + SinOscFB.ar(freq, mul: amp/2);

		// osc = osc + LPF.ar(Saw.ar(freq,mul:0.1),4000);

		env = EnvGen.ar(Env.perc(0.01, sus),doneAction:2);

		Out.ar(0,Pan2.ar( FreeVerb.ar(osc * env, mix:verb) , pan));
		} ).writeDefFile;

SynthDef.new( \dub,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		freq = freq / 4;

		amp = amp / 3;

		osc = LFTri.ar(freq, mul:amp) + SinOscFB.ar(freq,mul: amp);

		env = EnvGen.ar(Env.sine(sus),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \soft,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		amp = amp / 4;

		//freq = Vibrato.kr(freq, (freq/220), (freq/440) );

		osc =  SinOsc.ar(freq, mul:amp) + LFCub.ar(freq, mul:amp);

		env = EnvGen.ar(Env.perc(0.025, sus, curve:25 - (440/freq)),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \rev,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		amp = amp;

		osc =  SinOsc.ar(freq, mul:amp);

		env = EnvGen.ar(Env(times:[0.99 * sus, 0.01 * sus], curve:20), doneAction:2);

		Out.ar(0,Pan2.ar(FreeVerb.ar( osc * env ) , pan));
		} ).writeDefFile;

SynthDef.new( \organ,
	{
		arg amp=0,sus=1,pan=0,freq=0,atk=0.25;

		var osc, env;

		osc = LFPar.ar(freq, mul:amp / 8)  + LFSaw.ar(freq * 1/2 + 4, mul: amp * 1/100);

		env = EnvGen.ar(Env.perc(atk * sus, (1 - atk) * sus),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \sine,
	{
		arg amp=0,sus=1,pan=0,freq=0,atk=0.25,rate=1;

		var osc, env;

		osc = SinOsc.ar(freq, mul:SinOsc.ar(rate / 2) / 5);

		env = EnvGen.ar(Env.perc(atk * sus, (1 - atk) * sus),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \viola,
	{
		arg amp=0,sus=1,pan=0,freq=0,atk=0.25, vib=6, depth=0.008, verb=0.75;

		var osc, env, out;

		osc = PMOsc.ar(freq, Vibrato.kr(freq, rate:vib, depth:depth, delay: sus/8), 10, mul:amp / 8);

		env = EnvGen.ar(Env.perc(atk * sus, (1 - atk) * (sus * 3)),doneAction:2);

		out = env * osc;

		out = FreeVerb.ar(out, verb);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \distort,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env, ratio, tmp, out;

		ratio = 0.5;

		osc = LFPulse.ar(freq + 2, mul:amp * 0.125).distort * 2;

		env = EnvGen.ar(Env.perc(sus * 0.01, sus * 1),doneAction:2);

		tmp  = osc * env;

		osc = LFSaw.ar(freq - 2 , mul:amp * 0.25).distort * 2;

		env = EnvGen.ar(Env.perc(sus * 0.01, sus * 1), doneAction:2);

	  out = FreeVerb.ar((osc * env) + tmp, 0.33,0.75);

		Out.ar(0,Pan2.ar( out , pan));
		} ).writeDefFile;

SynthDef.new( \wiggle,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env,out;

		osc = LFSaw.ar(Vibrato.kr(freq,delay:sus/2,rate:6,depth:2,depthVariation:0), mul:amp/16);

		env = EnvGen.ar(Env(Array.series(15,0,1/15)++[0],Array.fill(14,sus/14)++[0]),doneAction:2);

		Out.ar(0,Pan2.ar(  osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \slide,
	{
		arg amp=0,sus=1,pan=0,freq=0,freq1=0;

		var osc, env;

		osc = LFTri.ar(Line.kr(freq1,freq + 4, 0.2 * sus), mul:amp/4) + SinOsc.ar(Line.kr(freq1,freq, 0.2 * sus), mul:amp/4) ;

		//osc = Slew.ar(osc,40,400);

		env = EnvGen.ar(Env(times:(sus * 0.5)!2),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;

SynthDef.new( \scratchy,
	{
		arg amp=0,sus=1,pan=0,freq=0,rate=0.04,depth=0.5;

		var osc, env;

		osc = SinOsc.ar(Vibrato.kr(freq * Crackle.ar(1.5), 2, 3, rateVariation:rate, depthVariation:depth), mul:amp  );

		env = EnvGen.ar(Env([0,amp / 16,0], [ sus, 0 ]), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).writeDefFile;


SynthDef.new( \speech2,
	{
		arg amp=0,sus=1,pan=0,freq=0,pos=0, verb=0.25, stretch=1, degree=0, dur=1, shift=0;

		var buf, env, rate, out, start;

		rate = 1.0 / sus;

		buf = Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/ryan/speech.wav", bufnum:99);
		env = EnvGen.ar(Env([0,1,1,0],[0,sus.abs,0]),doneAction:2);

		// Work out where to start playing

		start = BufSampleRate.kr(buf.bufnum) * stretch;

		shift = shift * start;

		pos = pos % (BufDur.kr(buf.bufnum) / stretch) * dur;

		start = start * pos;

		out = PlayBuf.ar(1,buf.bufnum, BufRateScale.kr(buf.bufnum), startPos: start + shift) * env * (amp * 10);

		// Change pitch

		out = PitchShift.ar(out, 0.1, 1 + (1/8 * (degree)), 0, 0.004);

		out = FreeVerb.ar(out, verb);

		Out.ar(0,Pan2.ar( out, pan));
		} ).writeDefFile;


SynthDef.new( \tone,
	{
		arg amp=0,sus=1,pan=0,freq=0,rate=1,depth=0.04,delay=0.01,onset=0,rateVar=0,depthVar=0,iphase=0;

		var osc, env, out;

		osc = SinOsc.ar(Vibrato.kr(freq, rate:rate - 1, depth:depth, delay:delay, onset:onset, rateVariation:rateVar, depthVariation:depthVar, iphase:iphase)) * 1/2;

		env = EnvGen.ar(Env(levels:[0,1,1,0]*(amp/2),times:[1/8,7/8,1/8]*sus),doneAction:2);

		out = (osc * env);

		Out.ar(0,Pan2.ar( out , pan));

} ).writeDefFile;


SynthDef(\klank,
	{
		arg pan=0, freq=440, sus=1,amp=1;
    var klank, n, harm, a, ring;

		sus=sus*1.5;

    // harmonics
		harm = [1,2,3,4];
    // amplitudes
    a = Array.fill(4, 0.5);
    // ring times
    ring =  Array.fill(4, 2);

		//{ClipNoise.ar(0.003)}.dup

		klank = Klank.ar(`[harm, a, ring], {ClipNoise.ar(0.0005)}.dup, freq);

		klank = klank * EnvGen.ar(Env([0,amp,0],[0.5 * sus, 0.5 * sus]),doneAction:2);

    Out.ar(0,Pan2.ar( klank , pan));
}).writeDefFile;


SynthDef.new( \soprano,
	{
		arg amp=0,sus=1,pan=0,freq=0,verb=0.5;

		var osc, env, vib;
		var klank, n, harm, a, ring;
		var freq1;

		freq1 = freq * 3;

		vib = Vibrato.kr(freq1, rate:5);

		osc = SinOsc.ar(vib, mul:amp / 2) + SinOscFB.ar(vib, mul:amp / 4);

		env = EnvGen.ar(Env([0,amp / 2,0],[sus / 2, sus / 2]), doneAction:2);

		// harmonics
		harm = [1,2,3,4];
		// amplitudes
		a = Array.fill(4, 0.5);
		// ring times
		ring =  Array.fill(4, 2);

		//{ClipNoise.ar(0.003)}.dup

		klank = Klank.ar(`[harm, a, ring], {ClipNoise.ar(0.0005)}.dup, freq);

		klank = klank * EnvGen.ar(Env([0,amp,0],[0.5 * sus, 0.5 * sus]),doneAction:2);

		Out.ar(0,Pan2.ar( FreeVerb.ar((osc * env) + klank, verb) , pan));
} ).writeDefFile;



// Bjorn Westergard
SynthDef(\pluck, {|freq = 440, dur = 1, sus=1, amp=1, pan=1|
	var klang,note;
	dur = dur * 2;
	amp = amp + 0.00001;
	note = freq.cpsmidi;
	note = note + (LFNoise2.ar(20).range(-1,1) * (1/8));
	klang = SinOsc.ar((note * [1,1.002]).midicps, phase: VarSaw.ar(note.midicps, width: Line.ar(1,0.2,dur))) * 0.3;
	klang = klang * XLine.ar(amp,(amp)/10000,sus*4) * 0.3;

	klang = klang * EnvGen.ar(Env([0,1,1,0],[0,sus*1.5,0]), doneAction:2);

	Out.ar(0, Pan2.ar( klang , pan));
}).writeDefFile;

SynthDef(\creep, {|freq = 440, dur = 1, sus=1, amp=1, pan=1|
	var klang,note;
	dur = dur * 2;
	amp = amp + 0.00001;
	note = freq.cpsmidi;
	note = note + (LFNoise2.ar(20).range(-1,1) * (1/8));
	klang = SinOsc.ar((note * [1,1.002]).midicps, phase: VarSaw.ar(note.midicps, width: Line.ar(1,0.2,dur)));
	// klang = klang * XLine.ar(amp,(amp)/10000,sus*4) * 0.3;

	klang = LPF.ar(klang, SinOsc.ar(freq));

	klang = klang * EnvGen.ar(Env([0,1,1,0],[0,sus,0]), doneAction:2) * amp * 5;

	Out.ar(0, Pan2.ar( klang , pan));
}).writeDefFile;

SynthDef(\arm, {|freq = 440, dur = 1, sus=1, amp=1, pan=1,rate=1|
	var klang,note,spin;
	dur = dur * 2;

	freq = freq;

	note = freq.cpsmidi;
	note = note + (LFNoise2.ar(20).range(-1,1) * (1/8));
	klang = LFSaw.ar((note * [1,1.002]).midicps);

	spin = SinOsc.ar(rate, mul:(freq/2), add:(freq));

	klang = LPF.ar(klang, spin);

	klang = klang * EnvGen.ar(Env.perc(releaseTime:sus,curve:4), doneAction:2) * (amp / 8);

	Out.ar(0, Pan2.ar( klang , SinOsc.ar(rate)));
}).add;

// From the default synth

SynthDef(\piano, { arg out=0, freq=440, amp=0.1, pan=0, gate=1, sus=1;
	var z;
	freq = freq*2;
	z = LPF.ar(
		Mix.new(
			VarSaw.ar(freq + [0, Rand(-0.4,0.0), Rand(0.0,0.4)], 0, 0.3, 0.3)),	XLine.kr(Rand(4000,5000), Rand(2500,3200), 1)
	) + FreeVerb.ar( VarSaw.ar(freq/2, width:0.1, mul:1), 0.5).distort;

	z = LPF.ar(z, freq, 1, 0, 0);


	z = z * EnvGen.ar(Env.perc(0.01, sus * 1.25,1,-4), doneAction:2);

	OffsetOut.ar(out, Pan2.ar(z, pan, amp / 2));
}, [\ir]).writeDefFile;

SynthDef(\siren, { |rate=1, sus = 1, freq=300|

	var son;
	var new_rate = rate/10;

	freq = LFPulse.kr(new_rate, 0.99, 0.4).lagud(0.4 / new_rate, 0.6 / new_rate) * 800 + freq;
	son  = LFPulse.ar(freq, 0.99, 0.2).lagud(0.4 / freq, 0.6 / freq) * 2 - 1;

	// This filtering is a simple approximation of the plastic horn acoustics:
	son = BPF.ar(son.clip2(0.2), 1500, 1/4) * 4;

	// delay and reverb, to simulate the environment in which we hear the siren
	son = son + DelayC.ar(son, 0.1, 0.1, 0.3);
	son = son + FreeVerb.ar(son);

	son = son * EnvGen.ar(Env([0,1,1,0],[0,sus/2,sus/2,0]),doneAction:2);

	Out.ar(0, Pan2.ar(son * 0.4));
}).writeDefFile;

SynthDef(\horn, { |rate=1, sus = 1, freq=300, pan=0|

	var osc1;
	var osc2;
	var new_rate = rate/10;

	osc1  = LFPulse.ar(Vibrato.kr(freq, freq / 5, 0.05), 0.99, 0.2).lagud(0.4 / freq, 0.6 / freq) * 2 - 1;

	osc2 = LFPulse.ar(freq/2, 0.5, 0.2).lagud(0.4 / freq, 0.6 / freq) * 2 - 1;


	// This filtering is a simple approximation of the plastic horn acoustics:
	osc1 = BPF.ar(osc1.clip2(0.2), 750, 1/4) * 4;
	osc2 = BPF.ar(osc2.clip2(0.8), 750, 1/4) * 4;

	// delay and reverb, to simulate the environment in which we hear the siren
	osc1 = osc1 + DelayC.ar(osc1, 0.1, 0.1, 0.3);
	osc1 = osc1 + FreeVerb.ar(osc1);
	osc2 = osc2 + DelayC.ar(osc2, 0.1, 0.1, 0.3);
	osc2 = osc2 + FreeVerb.ar(osc2);

	//son = son * EnvGen.ar(Env([0,1,0],[sus/2,sus/2,0]),doneAction:2);

	osc1 = osc1 * EnvGen.ar(Env.perc(0.1, sus, curve:-10), doneAction:2);
	osc2 = osc2 * EnvGen.ar(Env([0,1,0],[sus * 0.3, sus * 0.7])) * 0.5;

	osc1 = osc1 + osc2;

	Out.ar(0, Pan2.ar(osc1 * 0.6, pan));
}).writeDefFile;

SynthDef(\jazzbass, { |rate=1, sus = 1, freq=300,amp=1|

	var osc2;

	freq = freq / 4;

	osc2 = LFPulse.ar(freq, 0.5, 0.2).lagud(0.4 / freq, 0.6 / freq) * 2 - 1;

	osc2 = BPF.ar(osc2.clip2(0.8), freq , 1/4) * 4;

	osc2 = osc2 + DelayC.ar(osc2, 0.1, 0.1, 0.3);
	osc2 = osc2 + FreeVerb.ar(osc2);

	//son = son * EnvGen.ar(Env([0,1,0],[sus/2,sus/2,0]),doneAction:2);

	osc2 = osc2 * EnvGen.ar(Env.perc(0.05, sus, curve:-10), doneAction:2);

	Out.ar(0, Pan2.ar(osc2 * 0.4 * amp));
}).writeDefFile;

SynthDef(\grind, { |rate=1, sus = 1, freq=300, amp=1, pan=0|

	var son;

	son  = LFPulse.ar(Crackle.ar(2) * freq, 0.99, 0.2).lagud(0.4 / freq, 0.6 / freq) * 2 - 1;
	son = BPF.ar(son.clip2(0.2), 1500, 1/4) * 4;

	son = son + DelayC.ar(son, 0.1, 0.1, 0.3);
	son = son + FreeVerb.ar(son);

	son = son * EnvGen.ar(Env.perc(0.1, sus, curve:-10), doneAction:2);


	Out.ar(0, Pan2.ar(son * amp, pan));
}).writeDefFile;


SynthDef(\sweep, { |rate=1, sus = 1, freq=300, amp=1, pan=0|

	var son;

	son  = LFPulse.ar(Crackle.ar(1/4) * freq, 0, Line.ar(0,1,sus*2), 0.2) + VarSaw.ar(Crackle.ar(1/4) * freq + 1 * 2, 2, 2, 0.2, 0.3);

	// son = BPF.ar(son, 300, 10) * 2; SinOsc.ar(0.25 ,mul:freq*4,add:freq*5)

	son = LPF.ar([son, son + Crackle.ar()], XLine.ar(freq / 4, freq * 4, sus / 4) ) / 2;

	son = son + FreeVerb.ar(son);

	son = son * EnvGen.ar(Env.perc(sus / 16, sus * 2.5, curve:-10), doneAction:2);


	Out.ar(0, Pan2.ar(son * amp, pan));
}).writeDefFile;

SynthDef(\woop, { |rate=1, sus = 1, freq=300, amp=1, pan=0|

	var son;

	son  = LFTri.ar(Vibrato.kr(freq, rate, 1, rateVariation:1, depthVariation:0.5)) * LFPar.ar(Vibrato.kr(freq + 2, rate, 1, rateVariation:0.5, depthVariation:1)) * 1/5;

	son = son + DelayC.ar(son, 0.1, 1, 0.3);
	son = son + FreeVerb.ar(son,1,0.5);

	son = son * EnvGen.ar(Env.perc(0.1, sus, curve:-10), doneAction:2);


	Out.ar(0, Pan2.ar(son * amp, pan));
}).writeDefFile;


)
