SynthDef.new(\play1,
{|buf=0, pan=0, sus=1, rate=1.0, vib=0, fmod=0, freq=0, room=0.1, amp=1, pos=0, bus=0|
var osc, env;
rate = In.kr(bus, 1);
osc=PlayBuf.ar(1, buf, (BufRateScale.ir(buf) * rate), startPos: (BufSampleRate.kr(buf) * pos));
osc=(osc * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
