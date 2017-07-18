SynthDef.new(\play2,
{|vib=0, rate=1.0, sus=1, room=0.1, fmod=0, bus=0, amp=1, freq=0, buf=0, pan=0|
var osc, env;
rate = In.kr(bus, 1);
rate = Vibrato.kr(rate, rate: vib, depth: 0.05);
osc=PlayBuf.ar(2, buf, (BufRateScale.ir(buf) * rate));
osc=(osc * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
