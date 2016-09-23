FoxDot - Live Coding with Python v0.1.6
=======================================

*FoxDot is a pre-processed Python programming environment that provides a fast and user-friendly abstraction to SuperCollider. It also comes with its own IDE, which means it can be used straight out of the box; all you need is Python and SuperCollider and you're ready to go!*

### v0.1.6 fixes and updates
- Decimator (a.k.a. bitcrush) added to default SynthDef behaviour
- `SynthDefs` and `BufferManager` can be reloaded
- Removed automatic bootup of sclang as default behaviour
- Added new SynthDefs

See `docs/changelog` for more

---

## Installation and startup

#### Prerequisites
- [Python 2.7](https://www.python.org/downloads/release/python-2712/)
- [SuperCollider 3.6 and above](http://supercollider.github.io/download)

#### Recommended
- [sc3 plugins](http://sc3-plugins.sourceforge.net/)

#### Download and install

FoxDot uses the sound synthesis engine, SuperCollider, to make noise and Python 2.7 so you'll need to make sure they're installed correctly before using FoxDot. Download the `FoxDot-master.zip` file from this page and extract the contents. For the best experience, install the `UbuntuMono-R.ttf` font (optional).

#### Startup

1. Open SuperCollider
2. Open the file `FoxDot-Master/FoxDot/SCLang/OSCFunc.scd` in SuperCollider and execute the contents. This is done by placing the text cursor anywhere in the text and pressing `Ctrl+Return`. This boots the SuperCollider server (sometimes referred to as `sclang` or `SCLang` - short for SuperCollider Language) and listens for messages coming from FoxDot. 
3. Run the `main.py` file in the `FoxDot-master` directory. This can be done through the command line or by double-clicking the file, depending on how you've installed Python. To run FoxDot from the command line, change directory to `FoxDot-master` and enter the command `python main.py`

#### Troubleshooting

##### Buffer mismatch error
If you are getting an error along the lines of "Buffer UGen channel mismatch: expected 2, yet buffer has 1 channels" when trying to play back audio samples, go to FoxDot/Settings/Conf.txt and change the value of MAX_CHANNELS from 2 to 1 or vice versa. This issue might be to do with the version of SuperCollider or O/S being used.


## Basics

### Executing Code

A 'block' of code in FoxDot is made up of consecutive lines of code with no empty lines. Pressing `Ctrl+Return` will execute the block of code that the cursor is currently in. Try `print 1 + 1` to see what happens!

### Player Objects

Python supports many different programming paradigms, including procedural and functional, but FoxDot implements a traditional object orientated approach with a little bit of cheating to make it easier to live code. Player objects are created when the FoxDot library is imported and are assigned to all possible one or two character variable names. By using a double-arrow, `>>`, operator like so:

	p1 >> synth([0,1,2,3])

The empty player object, `p1` is now assigned a particular synth and playback instructions. `p1` will play the first four notes of the default scale using a SuperCollider `SynthDef` with the name `\synth`. By default, each note lasts for 1 beat at 120 bpm. These defaults can be changed by specifying keyword arguments:

	p1 >> synth([0,1,2,3], dur=[1/4,3/4], sus=1, rate=4, scale=Scale.minor)

The keyword arguments `dur`, `oct`, and `scale` apply to all player objects - any others, such as `rate` in the above example, refer to keyword arguments in the corresponding `SynthDef`. The first argument, `degree`, does not have to be stated explicitly. Notes can be grouped together so that they are played simultaneously using round brackets, `()`. The sequence `[(0,2,4),1,2,3]` will play the the the first harmonic triad of the default scale followed by the next three notes. To see a list of the FoxDot SynthDefs, simply execute `print SynthDefs`.

### 'Sample Player' Objects

In FoxDot, sound files can be played through using a specific SynthDef called `play`. A player object that uses this SynthDef is referred to as a Sample Player object. Instead of specifying a list of numbers to generate notes, the Sample Player takes a string of characters as its first argument. Each character in the string refers to one sample (the current list can be seen in the `FoxDot/Settings/samplelib.csv` file, which you can customise if you so wish). To create a basic drum beat, you can execute the following line of code:

	d1 >> play("x-o-")

To have samples play simultaneously, just create a new 'Sample Player' object for some more complex patterns.

	bd >> play("x( x)  ")
	hh >> play("---[--]")
	sn >> play("  o ")

Grouping characters in round brackets laces the pattern so that on each play through of the sequence of samples, the next character in the group's sample is played. The sequence `(xo)---` would be played back as if it were entered `x---o---`. Characters in square brackets are played twice as fast (half the duration) of one character by itself, and characters in curly brackets (`{}`) are played in the same time span as one character. Example: `{oo}` would play two snare hits at a quarter beat each but `{ooo}` would play three snare hits at 3/8 beats each.

## Writing your own Synth Definitions

FoxDot can access any `SynthDef` stored on the SuperCollider server but you may want to write (or edit) your own during run-time in FoxDot. This is done using the `SCLang` module. All FoxDot `SynthDef` objects inherit the base-class behaviour, such as low- and high-pass filters and vibrato, but these can be overridden or updated easily. The `SCLang` module also provides an easy-to-use API to the SCLang used in SuperCollider

Example:

```python
# Import module for writing SCLang code from Python
from SCLang import *

# Create a SynthDef named 'example'
ex = SynthDef("example")			

# Add a custom argument named 'pow'
ex.defaults.update(pow=1)			

# Create our oscillator using a sine wave that oscillates at the given frequency to power of 'pow'
ex.osc = SinOsc.ar(ex.freq ^ ex.pow)	

# Using a percussive sound envelope
ex.env = Env.perc()					

# Add to the server
ex.add()							
```

*This is equivalent to the following SynthDef that inherits from the base-class (it's a little nicer isn't it?)*

```java
SynthDef.new( \example,
	{ |vib=0, vibVar=0.04, pow=1, echo=0, depthVar=0.1, vibDelay=0, slide=0, delay=0, sus=1, hpf=0, pan=0, scrub=0, verb=0.25, amp=1, freq=0, buf=0, echoOn=0, room=0.5, rate=0, depth=0.02, grain=0, lpf=20000, slidefrom=1|

	var osc, env;

	freq=Vibrato.kr(Line.ar((freq * slidefrom), (freq * (1 + slide)), sus), delay: vibDelay, depthVariation: depthVar, rate: vib, rateVariation: vibVar, depth: depth);

	osc=LPF.ar(HPF.ar(SinOsc.ar((freq ** pow)), hpf), lpf);

	env=EnvGen.ar(Env.perc(level: amp, releaseTime: sus).delay(delay), doneAction: 2);

	Out.ar(0, Pan2.ar(FreeVerb.ar(((osc + (echoOn * CombN.ar(osc, (echo * 0.1), (echo * 0.1), ((echo * 0.5) * sus), 1))) * env), verb, room), pan))}).add;
```

The attribute `env` is set to `Env.perc()` by default, so as long as you set `osc` to a valid SuperCollider UGen, you'll be making noise in no time! Once the `SynthDef` has been added to the server, you'll be able to use it using the basic FoxDot syntax like so:

	e1 >> ex([0,1,2,3], pow=[1,1.5])


## Documentation

For more information on FoxDot, please see http://foxdot.org/
