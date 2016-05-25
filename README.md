FoxDot - Live Coding with Python v0.1.2
=======================================

*FoxDot is a pre-processed Python-based programming language that provides a fast and user-friendly abstraction to SuperCollider. It also comes with its own IDE, which means it can be used straight out of the box and no fiddling around with config files; all you need is Python and SuperCollider and you're ready to go!*

---

## Installation and startup

*Note: FoxDot is still in early development and has only been tested with Python 2.7, SuperCollider 3.6.6, with Windows 7 and Windows 8.*

FoxDot uses the sound synthesis engine, SuperCollider, to make music so you'll need to make sure it's installed before using FoxDot. Currently, all you need to do is download the `.zip` file from this page and extract the contents. To start using FoxDot, first make sure you have a SuperCollider server instance running on your local machine (open SuperCollider and press `Ctrl+b`) then run `main.py` from the FoxDot folder. FoxDot can access any `SynthDef` that's stored on the server but it comes with some built-in definitions that are written in Python (more on that later). To use these, execute the following snippet of code (also found in `foxdot.scd`) or, better yet, add it to your `startup.scd` file that's located in your SuperCollider installation folder so that it's automatically executed when you boot SuperCollider.

```java
(
OSCFunc(
	{
    arg msg, time, addr, port;
		msg[1].asString.interpret;  // will execute the string sent from FoxDot
		msg[1].postln;
	},
	'foxdot'
);
)
```

## Basics

### Executing Code

A 'block' of code in FoxDot is made up of consecutive lines of code with no empty lines. Pressing `Ctrl+Return` will execute the block of code that the cursor is currently in. Try `print 1 + 1` to see what happens!

### Player Objects

Python supports many different programming paradigms, including procedural and functional, but FoxDot implements a traditional object orientated approach. Player objects are created like most objects in Python, by assigning them to a variable name. What makes FoxDot different, however, is that instead of using the `=` operator (e.g. `a = class()`), player objects are created using a double-arrow, `>>`, operator like so:

	player >> synth([0,1,2,3])

This player object, `player`, now plays the first four notes of the default scale using a `SynthDef` with the name `\synth`. By default, each note lasts for 1 beat at 120 bpm (see default for more). These defaults can be changed by specifying keyword arguments:

	player >> synth([0,1,2,3], dur=[1/4,3/4], sus=1, rate=4, scale=Scale.minor)

The keyword arguments `dur`, `oct`, and `scale` apply to all player objects - any others, such as `rate` in the above example, refer to keyword arguments in the corresponding `SynthDef`. The first argument, `degree`, does not have to be stated explicitly. Notes can be grouped together so that they are played simultaneously using round brackets, `()`. The sequence `[(0,2,4),1,2,3]` will play the the the first harmonic triad of the default scale followed by the next three notes. To see a list of the FoxDot SynthDefs, simply execute `print SynthDefs`.

### 'Sample Player' Objects

In FoxDot, sound files can be played through using 'Sample Player' objects. These are created by assigning a string of characters to a variable using the `$` sign. Each character in the string refers to one sample (the current list can be seen in the `Samples/config.txt` file, which you can customise if you so wish). To create a basic drum beat, you can execute the following line of code:

	drums $ "x-o-"

To have samples play simultaneously, just create a new 'Sample Player' object for some more complex patterns.

	bd $ "x( x)   "
	hh $ "---[--]"
	sn $ "  o "

Grouping characters in round brackets laces the pattern so that on each play through of the sequence of samples, the next character in the group's sample is played. The sequence `(xo)---` would be played back as if it were entered `x---o---`. Characters in square brackets are played twice as fast (half the duration) of one character by itself, and characters in curly brackets (`{}`) are played in the same time span as one character. Example: `{oo}` would play two snare hits at a quarter beat each but `{ooo}` would play three snare hits at 3/8 beats each.

## Writing your own Synth Definitions

FoxDot can access any `SynthDef` stored on the SuperCollider server but you may want to write (or edit) your own during run-time in FoxDot. This is done using the `SCLang` module (the contents are imported on startup). All FoxDot `SynthDef` objects inherit the base-class behaviour, such as low- and high-pass filters and vibrato, but these can be overridden or updated easily. The `SCLang` module also provides an easy-to-use API to the SCLang used in SuperCollider

Example:

```python
# Create a SynthDef named 'example'
ex = SynthDef("example")			

# Add a custom argument named 'pow'
ex.defaults.update(pow=1)			

# Create our oscillator using a sine wave that oscillates at the given frequency to power of 'pow'
ex.osc = SinOsc.ar(freq ^ ex.pow)	

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

	out >> example([0,1,2,3], pow=[1,1.5])


## Undocumented Items

* Patterns
* TimeVar
* Scale
* Root
* When Statements
* Clock
