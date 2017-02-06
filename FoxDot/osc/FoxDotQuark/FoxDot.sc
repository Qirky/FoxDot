FoxDot
{

	classvar server;

	*start
	{

		server = Server.default;

		server.options.memSize = 8192 * 16; // increase this if you get "alloc failed" messages
		server.options.maxNodes = 1024 * 32; // increase this if you are getting drop outs and the message "too many nodes"
		server.options.numOutputBusChannels = 2; // set this to your hardware output channel size, if necessary
		server.options.numInputBusChannels = 2; // set this to your hardware output channel size, if necessary
		server.boot();


		OSCFunc(
			{
				arg msg, time, addr, port;
				var fn, load;

				// Get local filename

				fn = msg[1].asString;

				// Add SynthDef to file

				fn = File(fn, "r");
				fn.readAllString.interpret;
				fn.close;

			},
			'foxdot'
		);

		StageLimiter.activate(2);

		"Listening for messages from FoxDot".postln;
	}
}