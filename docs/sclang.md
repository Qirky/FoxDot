# SCLang

## Classes

### SynthDef

	SynthDef.__init__(self, name)

desc

	SynthDef.add(self)

desc

	SynthDef.__call__(self, degree=0, **kwargs)

desc

## Writing your own Synth Definitions

FoxDot can access any SynthDef stored on the SuperCollider server, but it needs to know it's there. If you have already written a SynthDef in SuperCollider and named it `\mySynth` then you just create a SynthDef instance using FoxDot like so:

``` python
mySynth = SynthDef("mySynth")
```

Using the same variable name in FoxDot as in SuperCollider for your SynthDef is a good idea to avoid confusion. If you want to write (or edit) your own SynthDef during run-time in FoxDot you can use a SuperCollider API by importing the `SCLang` module. All FoxDot SynthDef objects inherit the base-class behaviour, such as low- and high-pass filters and vibrato, but these can be overridden or updated easily. If you want to know more about digital sound processing and SynthDef creation, check out the [SuperCollider documentation](http://doc.sccode.org/Classes/SynthDef.html). Below is an example of creating one in FoxDot:

``` python
# Import module for writing SCLang code from Python
from SCLang import *

# Create a SynthDef named 'example' (using the same variable name as the SynthDef name is a good idea)
example = SynthDef("example")				

# Create the oscillator (osc) using a sine wave
example.osc = SinOsc.ar(ex.freq)	

# And give it a percussive sound envelope (env)
example.env = Env.perc()					

# Finally, store it!
example.add()							
```

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
