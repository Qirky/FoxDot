s.nextNodeID

(

// Below we outline the buffer numbers for each sample

Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/bd1.wav", bufnum: 1); // Bass drum 1
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/bd2.wav", bufnum: 2); // Bass drum 2
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/sd1.wav", bufnum: 3); // Snare drum 1
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/sd2.wav", bufnum: 4); // Snare drum 2
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/cp1.wav", bufnum: 5); // Clap
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/hhc.wav", bufnum: 6); // hi hat closed
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/hho.wav", bufnum: 7); // hi hat open
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/cb1.wav", bufnum: 8); // Cowbell
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/cs1.wav", bufnum: 9); // Cross stick
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/no1.wav", bufnum: 10); // Noise burst
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/kk1.wav", bufnum: 11); // House kick 1
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/kk2.wav", bufnum: 12); // House kick 2
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/sh1.wav", bufnum: 13); // Shaker (tambourine)
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/rd1.wav", bufnum: 14); // Ride
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/ck1.wav", bufnum: 15); // Clicks
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/tm1.wav", bufnum: 16); // Tom tom
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/cr1.wav", bufnum: 17); // Crash
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/foxdot/sw1.wav", bufnum: 18); // Swoop

// Buffers for the toplap manifesto draft

Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/ryan/this.wav", bufnum: 50);
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/ryan/too.wav", bufnum: 51);
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/ryan/shall.wav", bufnum: 52);
Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/ryan/pass.wav", bufnum: 53);
// Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/toplap/fest.wav", bufnum: 54);
// Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/toplap/o.wav", bufnum: 55);
// Buffer.read(s,thisProcess.nowExecutingPath.dirname +/+ "samples/toplap/draft.wav", bufnum: 56);

// Create sample player synth

SynthDef.new( \sample_player,
	{
		arg buf=0,amp=1,pan=0,rate=1, sus=1;
		var sound, verb;

		verb = 0.2;
		sound = FreeVerb.ar( PlayBuf.ar(1, buf, BufRateScale.ir(buf) * rate) * amp * 2 , 0.2, 0.1);

		sound = sound * EnvGen.ar(Env([0,1,1,0],[0 ,sus * 2, 0]), doneAction:2);

		Out.ar(0,Pan2.ar( sound , pan));
		} ).add;


SynthDef.new( \words,
	{
		arg pos=0,amp=1,pan=0,rate=1;
		var buf;
		buf = 50 + pos;
		Out.ar(0,Pan2.ar( PlayBuf.ar(1, buf, BufRateScale.ir(buf) * rate, doneAction:2) * amp * 2 , pan));
		} ).add;


// Create synthdef with musical input

SynthDef.new( \crunch,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		osc = LFNoise0.ar(Crackle.kr(1.95) * 6000, mul: amp);

		env = EnvGen.ar(Env.perc(0.01,0.1,amp / 2), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).add;

SynthDef.new( \rave,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		osc = Gendy1.ar(freq, mul:amp/2) ;

		env = EnvGen.ar(Env.perc(0.01, sus), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
} ).add;


SynthDef.new( \pads,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		osc = SinOsc.ar(freq, mul:amp / 2) + SinOsc.ar(freq + 2, mul:amp / 8) ;

		env = EnvGen.ar(Env.perc(0.01, sus), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
} ).add;

SynthDef.new( \banjo,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		osc = Formant.ar(freq, mul:amp/2) + LFSaw.ar(freq, mul:amp/25);

		env = EnvGen.ar(Env.perc(0.01, sus), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
} ).add;


SynthDef.new( \bell,
	{
		|freq=465, strength=1, decay=3, sus=1,amp=1|
		var son;
		son = Klank.ar(`[
			// frequency ratios
			[0.501, 1, 0.7,   2.002, 3, 9.6,   2.49, 11, 2.571,  3.05, 6.242, 12.49, 13, 16, 24],
			// amps
			[0.002,0.02,0.001, 0.008,0.02,0.004, 0.02,0.04,0.02, 0.005,0.05,0.05, 0.02, 0.03, 0.04],
			// ring times - "stutter" duplicates each entry threefold
			[1.2, 0.9, 0.25, 0.14, 0.07].stutter(3)
			]
			, Impulse.ar(1), freq, 0, decay);

		son = son * EnvGen.ar(Env([0,1,1,0],[0 ,sus*3, 0]), doneAction:2) * amp * 1.5;
		Out.ar(0, Pan2.ar(son));
}).add;

SynthDef.new( \soprano,
	{
		arg amp=0,sus=1,pan=0,freq=0,verb=0.5,freq1=0;

		var osc, env, vib;

		if ( (freq1 != 0), { freq1 = freq; }, { freq1 = freq1});

		vib = Vibrato.kr(Line.kr(freq1, freq, sus), rate:5);

		osc = SinOsc.ar(vib, mul:amp / 2) + SinOscFB.ar(vib, mul:amp / 4);

		env = EnvGen.ar(Env([0,amp / 2,0],[sus / 2, sus / 2]), doneAction:2);

		Out.ar(0,Pan2.ar( FreeVerb.ar(osc * env, verb) , pan));
		} ).add;

SynthDef.new( \bass,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env;

		amp = amp / 5;

		osc = LFTri.ar(freq, mul:amp) + SinOscFB.ar(freq,mul: amp) + LFSaw.ar(freq, mul: amp);

		env = EnvGen.ar(Env.perc(0.01, sus),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).add;

SynthDef.new( \organ,
	{
		arg amp=0,sus=1,pan=0,freq=0,atk=0.25;

		var osc, env;

		osc = LFPar.ar(freq, mul:amp / 8)  + LFSaw.ar(freq * 1/2 + 4, mul: amp * 1/100);

		env = EnvGen.ar(Env.perc(atk * sus, (1 - atk) * sus),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).add;

SynthDef.new( \sine,
	{
		arg amp=0,sus=1,pan=0,freq=0,atk=0.25;

		var osc, env;

		osc = SinOsc.ar(freq, mul:amp / 2);

		env = EnvGen.ar(Env.perc(atk * sus, (1 - atk) * sus),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).add;

SynthDef(\siren, { |rate=1, sus = 1|

	var new_rate = rate/10;

	var freq = LFPulse.kr(new_rate, 0.99, 0.4).lagud(0.4 / new_rate, 0.6 / new_rate) * 800 + 300;
	var son  = LFPulse.ar(freq, 0.99, 0.2).lagud(0.4 / freq, 0.6 / freq) * 2 - 1;

	// This filtering is a simple approximation of the plastic horn acoustics:
	son = BPF.ar(son.clip2(0.2), 1500, 1/4) * 4;

	// delay and reverb, to simulate the environment in which we hear the siren
	son = son + DelayC.ar(son, 0.1, 0.1, 0.3);
	son = son + FreeVerb.ar(son);

	son = son * EnvGen.ar(Env([0,1,1,0],[0,sus/2,sus/2,0]),doneAction:2);

	Out.ar(0, Pan2.ar(son * 0.4));
}).add;

SynthDef.new( \viola,
	{
		arg amp=0,sus=1,pan=0,freq=0,atk=0.25, vib=6, depth=0.008, verb=0.75;

		var osc, env, out;

		osc = PMOsc.ar(freq, Vibrato.kr(freq, rate:vib, depth:depth, delay: sus/8), 10, mul:amp / 8);

		env = EnvGen.ar(Env.perc(atk * sus, (1 - atk) * (sus * 3)),doneAction:2);

		out = env * osc;

		out = FreeVerb.ar(out, verb);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).add;

SynthDef.new( \distort,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env, ratio, tmp, out;

		ratio = 0.5;

		osc = LFPulse.ar(freq + 2, mul:amp * 0.25).distort * 2;

		env = EnvGen.ar(Env.perc(sus * 0.1, sus * 0.9),doneAction:2);

		tmp  = osc * env;

		osc = Impulse.ar(freq - 2 , mul:amp * 0.5).distort * 2;

		env = EnvGen.ar(Env.perc(sus * 0.9, sus * 0.1), doneAction:2);

		out = FreeVerb.ar((osc * env) + tmp, 0.33,0.75);

		Out.ar(0,Pan2.ar( out , pan));
		} ).add;

SynthDef.new( \wiggle,
	{
		arg amp=0,sus=1,pan=0,freq=0;

		var osc, env,out;

		osc = LFSaw.ar(Vibrato.kr(freq,delay:sus/2,rate:6,depth:2,depthVariation:0), mul:amp/16);

		env = EnvGen.ar(Env(Array.series(15,0,1/15)++[0],Array.fill(14,sus/14)++[0]),doneAction:2);

		Out.ar(0,Pan2.ar(  osc * env , pan));
		} ).add;

SynthDef.new( \slide,
	{
		arg amp=0,sus=1,pan=0,freq=0,freq1=0;

		var osc, env;

		osc = LFTri.ar(Line.kr(freq1,freq + 4, 0.2 * sus), mul:amp/4) + SinOsc.ar(Line.kr(freq1,freq, 0.2 * sus), mul:amp/4) ;

		//osc = Slew.ar(osc,40,400);

		env = EnvGen.ar(Env(times:(sus * 0.5)!2),doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).add;

SynthDef.new( \scratchy,
	{
		arg amp=0,sus=1,pan=0,freq=0,rate=0.04,depth=0.5;

		var osc, env;

		osc = SinOsc.ar(Vibrato.kr(freq * Crackle.ar(1.5), 2, 3, rateVariation:rate, depthVariation:depth), mul:amp  );

		env = EnvGen.ar(Env([0,amp / 16,0], [ sus, 0 ]), doneAction:2);

		Out.ar(0,Pan2.ar( osc * env , pan));
		} ).add;


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
		} ).add;


SynthDef.new( \tone,
	{
		arg amp=0,sus=1,pan=0,freq=0,rate=1,depth=0.04,delay=0.01,onset=0,rateVar=0,depthVar=0,iphase=0;

		var osc, env, out;

		osc = SinOsc.ar(Vibrato.kr(freq, rate:rate - 1, depth:depth, delay:delay, onset:onset, rateVariation:rateVar, depthVariation:depthVar, iphase:iphase)) * 1/2;

		env = EnvGen.ar(Env(levels:[0,1,1,0]*(amp/2),times:[1/8,7/8,1/8]*sus),doneAction:2);

		out = (osc * env);

		Out.ar(0,Pan2.ar( out , pan));

} ).add;


SynthDef(\klank,
	{
		arg pan=0, freq=440, sus=1,amp=1;
    var klank, n, harm, a, ring;

    // harmonics
		harm = [1,2,3,4];
    // amplitudes
    a = Array.fill(4, 0.5);
    // ring times
    ring =  Array.fill(4, 2);

		//{ClipNoise.ar(0.003)}.dup

		klank = Klank.ar(`[harm, a, ring], {ClipNoise.ar(0.0005)}.dup, freq);

		klank = klank * EnvGen.ar(Env([0,amp/2,0],[0.5 * sus, 0.5 * sus]),doneAction:2);

    Out.ar(0,Pan2.ar( klank , pan));
}).add;



// Bjorn Westergard
SynthDef(\pluck, {|freq = 440, dur = 1, sus=1, amp=1, pan=1|
	var klang,note;
	dur = dur * 2;
	note = freq.cpsmidi;
	note = note + (LFNoise2.ar(20).range(-1,1) * (1/8));
	klang = SinOsc.ar((note * [1,1.002]).midicps, phase: VarSaw.ar(note.midicps, width: Line.ar(1,0.2,dur))) * 0.3;
	klang = klang * XLine.ar(amp,(amp)/10000,sus,doneAction:2) * 0.3;
	Out.ar(0, Pan2.ar( klang , pan));
}).add;


)