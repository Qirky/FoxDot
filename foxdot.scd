(
OSCFunc(
	{
    arg msg, time, addr, port;
		msg[1].asString.interpret;  //will execute the string sent from python
		msg[1].postln;
	},
	'foxdot'
);
)