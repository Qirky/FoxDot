(
OSCFunc(
	{
		arg msg, time, addr, port;
		var flag, path;

		// Get  filename

		flag = msg[1];

		path = msg[2].asString;

		// Print a message to the user

		("Started recording to" + path).postln;

		// Record or stop / recording

		if (flag==1,
			{s.record(path)},
			{s.stopRecording()},
		);

	},
	'foxdot-record'
);
)

