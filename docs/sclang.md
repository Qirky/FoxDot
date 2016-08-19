# SCLang

## Classes

### SynthDef

	SynthDef.__init__(self, name)

desc

	SynthDef.add(self)

desc

	SynthDef.__call__(self, degree=0, **kwargs)

desc

#### How to create a SynthDef

	with SynthDef("pads") as pads:
		pads.osc = SinOsc.ar(pads.freq)
		pads.env = Env.perc()

Equivalent to

	pads = SynthDef("pads")
	pads.osc = SinOsc.ar(pads.freq)
	pads.env = Env.perc()
	pads.add()

desc

### SynthDefProxy

	SynthDefProxy.__init__(self, name, degree, kwargs)

desc

### Env

	Env.__call__(self, *args, **kwargs)

desc

	Env.block
	Env.reverse

desc

## Pseudo-Classes

desc

	SinOsc
	SinOscFB
	Saw
	LFSaw
	VarSaw
	LFTri
	LFPar
	PlayBuf
	LFNoise0
	LFNoise1
	LFNoise2
	Gendy1
	Gendy2
	Gendy3
	Gendy4
	Gendy5
	Formant
	Pulse
	LFPulse
	PMOsc
	Crackle
	LFCub
	PinkNoise
	Impulse
	Klank
	Out
	Vibrato
	Line
	XLine
	FreeVerb
	GVerb
	Pan2
	LPF
	BPF
	HPF
	DelayC
	CombN
	Crackle
	ClipNoise
	BufRateScale
	BufChannels
	BufFrames
