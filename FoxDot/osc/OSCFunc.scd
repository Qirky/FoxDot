(
s.options.blockSize = 128;
s.options.memSize = 131072;
s.boot;

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
)