(
OSCFunc(
	{
		arg msg, time, addr, port;
		var fn;

		// Get local filename

		fn = msg[1].asString;

		// Print a message to the user

		("Loading SynthDef from" + fn).postln;

		// Add SynthDef to file

		fn = File(fn, "r");
		fn.readAllString.interpret;
		fn.close;

	},
	'foxdot'
);
)