SynthDef.new(\loop,
{|vib=0, rel=0.01, bus=0, pos=0, sample=0, rate=1.0, peak=1, amp=1, freq=0, buf=0, beat_dur=1, room=0.1, decay=0.01, level=0.8, atk=0.01, sus=1, fmod=0, blur=1, pan=0|
var osc, env;
sus = sus * blur;
rate = In.kr(bus, 1);
osc = PlayBuf.ar(2, buf, BufRateScale.kr(buf) * rate, startPos: BufSampleRate.kr(buf) * pos, loop: 1.0);
osc = osc * EnvGen.ar(Env([0,1,1,0],[0.05, sus-0.05, 0.05]));
osc=(osc * amp);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc)}).add;
