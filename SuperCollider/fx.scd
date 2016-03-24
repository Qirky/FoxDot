(
// define an echo effect
SynthDef("echo", { arg sus, delay = 0.2, decay = 4;
	var in, out;
	in = In.ar(0,2);
	out = CombN.ar(in, 0.5, delay, decay, 1, in);
	out = out * EnvGen.ar(Env([0,1,1,0],[0 , sus , 0]), doneAction:2);
	// use ReplaceOut to overwrite the previous contents of the bus.
	ReplaceOut.ar(0, out);
}).send(s);

// define a reverb effect
SynthDef("reverb", { arg sus, mix=0.33, room=0.5, damp=0.5;
	var in;
	in = In.ar(0,2);
	// use ReplaceOut to overwrite the previous contents of the bus.
	ReplaceOut.ar(0, FreeVerb.ar(in, mix, room, damp));
}).send(s);

)