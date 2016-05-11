FoxDot - Live Coding with Python v0.1
=====================================

*FoxDot is a pre-processed Python-based programming language that provides a fast and user-friendly abstraction to SuperCollider. It also comes with its own IDE, which means it can be used straight out of the box and no fiddling around with config files; all you need is Python and SuperCollider and you're ready to go!*

---

## Installation and startup

*Note: FoxDot is still in early development and has only been tested with Python 2.7, SuperCollider 3.6.6, with Windows 7 and Windows 8.*

Currently, all you need to do is download the `.zip` file from this page and extract the contents. To start using FoxDot, first make sure you have a SuperCollider server instance running on your local machine then run `main.py` from the FoxDotCode folder. FoxDot can use any `SynthDef` that's stored on the server but there are some examples in `SuperCollider/startup.scd` that demonstrate some of the best practices for combining FoxDot with SuperCollider.

## Basics

### Executing Code

A 'block' of code in FoxDot is made up of consecutive lines of code with no empty lines. Pressing `Ctrl+Return` will execute the block of code that the cursor is currently in. Try `print 1 + 1` to see what happens!

### Player Objects

Python supports many different programming paradigms, including procedural and functional, but FoxDot implements a traditional object orientated approach. Player objects are created like most objects in Python, by assigning them to a variable name. What makes FoxDot different, however, is that instead of using the `=` operator (e.g. `a = class()`), player objects are created using a double-arrow, `>>`, operator like so:

	player >> synth([0,1,2,3])

This player object, `player`, now plays the first four notes of the default scale using a `SynthDef` with the name `\synth`. By default, each note lasts for 1 beat at 120 bpm (see default for more). These defaults can be changed by specifying keyword arguments:

	player >> synth([0,1,2,3], dur=[1/4,3/4], sus=1, rate=4, scale=Scale.minor)

The keyword arguments `dur`, `oct`, and `scale` apply to all player objects - any others, such as `rate` in the above example, refer to keyword arguments in the corresponding `SynthDef`. The first argument, `degree`, does not have to be stated explicitly. Notes can be grouped together so that they are played simultaneously using round brackets, `()`. The sequence `[(0,2,4),1,2,3]` will play the the the first harmonic triad of the default scale followed by the next three notes.

### 'Sample Player' Objects

In FoxDot, sound files can be played through using 'Sample Player' objects. These are created by assigning a string of characters to a variable using the `$` sign. Each character in the string refers to one sample (the current list can be seen in the `Samples/config.txt` file, which you can customise if you so wish). To create a basic drum beat, you can execute the following line of code:

	drums $ "x-o-"

To have samples play simultaneously, just create a new 'Sample Player' object for some more complex sounds.

	bd $ "x( x)   "
	hh $ "---[--]"
	sn $ "  o "

Grouping characters in round brackets laces the pattern so that on each play through of the sequence of samples, the next character in the group's sample is played. The sequence `(xo)---` would be played back like `x---o---`. Characters in  square brackets are played in the same time span as one character by itself.

## Best Practices

### SuperCollider SynthDefs

Custom `SynthDefs` should contain the following keyword arguments:

* `amp` - A value between 0 (silent) and 1 (loud)
* `pan` - A value between -1 (left) and 1 (right) 
* `sus` - The duration of a note, and should be included in an `EnvGen`
* `freq` - The frequency of the sound

## Undocumented Items

* Patterns
* TimeVar
* Default
* Fx
* Best practice
* when statements