SynthDef.new(\loop,
{|vib=0, bus=0, pos=0, rate=1.0, amp=1, freq=0, buf=0, room=0.1, sus=1, fmod=0, pan=0|
var osc, env;
rate = In.kr(bus, 1);
osc = PlayBuf.ar(2, buf, BufRateScale.kr(buf) * rate, startPos: BufSampleRate.kr(buf) * pos);
osc = osc * EnvGen.ar(Env([0,1,1,0],[0.05, sus-0.05, 0.05]));
osc=(osc * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
