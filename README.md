FoxDot - Live Coding with Python v0.1.8
=======================================

*FoxDot is a pre-processed Python programming environment that provides a fast and user-friendly abstraction to SuperCollider. It also comes with its own IDE, which means it can be used straight out of the box; all you need is Python and SuperCollider and you're ready to go!*

### v0.1.8 fixes and updates

- PSparse pattern type added (all Pattern names can be seen by executing `print(PatternTypes)`
- Major overhaul of Pattern nesting/lacing behaviour. Patterns can now be nested to multiple levels.
- Player object attributes now 'follow' one another and their current  values are examined instead of the Pattern value

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

A 'block' of code in FoxDot is made up of consecutive lines of code with no empty lines. Pressing `Ctrl+Return` (or `Cmd-Return` on a Mac) will execute the block of code that the cursor is currently in. Try `print 1 + 1` to see what happens!

### Player Objects

Python supports many different programming paradigms, including procedural and functional, but FoxDot implements a traditional object orientated approach with a little bit of cheating to make it easier to live code. A player object is what FoxDot uses to make music by assigning it a synth (the 'instrument' it will play) and some instructions, such as note pitches. All one and two character variable names are reserved for player objects at startup so, by default, the variables `a`, `bd`, and `p1` are 'empty' player objects. If you use one of these variables to store something else but want to use it as a player object again, or you  want to use a variable with more than two characters, you just have to reserve it by creating a `Player` and assigning it like so:

``` python
p1 = Player()
```

Assigning synths and instructions to a player object is done using the double-arrow operator `>>`. So if you wanted to assign a synth to `p1` called 'pads' (execute `print SynthDefs` to see all available synths) you would use the following code:

``` python
p1 >> pads([0,1,2,3])
```

The empty player object, `p1` is now assigned a the 'pads' synth and some playback instructions. `p1` will play the first four notes of the default scale using a SuperCollider `SynthDef` with the name `\pads`. By default, each note lasts for 1 beat at 120 bpm. These defaults can be changed by specifying keyword arguments:

``` python
p1 >> pads([0,1,2,3], dur=[1/4,3/4], sus=1, rate=4, scale=Scale.minor)
```

The keyword arguments `dur`, `oct`, and `scale` apply to all player objects - any others, such as `rate` in the above example, refer to keyword arguments in the corresponding `SynthDef`. The first argument, `degree`, does not have to be stated explicitly. Notes can be grouped together so that they are played simultaneously using round brackets, `()`. The sequence `[(0,2,4),1,2,3]` will play the the the first harmonic triad of the default scale followed by the next three notes. 

### 'Sample Player' Objects

In FoxDot, sound files can be played through using a specific SynthDef called `play`. A player object that uses this SynthDef is referred to as a Sample Player object. Instead of specifying a list of numbers to generate notes, the Sample Player takes a string of characters as its first argument. Each character in the string refers to one sample (the current list can be seen in the `FoxDot/Settings/samplelib.csv` file, which you can customise if you so wish). To create a basic drum beat, you can execute the following line of code:

``` python
d1 >> play("x-o-")
```

To have samples play simultaneously, just create a new 'Sample Player' object for some more complex patterns.

``` python
bd >> play("x( x)  ")
hh >> play("---[--]")
sn >> play("  o ")
```

Grouping characters in round brackets laces the pattern so that on each play through of the sequence of samples, the next character in the group's sample is played. The sequence `(xo)---` would be played back as if it were entered `x---o---`. Characters in square brackets are played twice as fast (half the duration) of one character by itself, and characters in curly brackets (`{}`) are played in the same time span as one character. Example: `{oo}` would play two snare hits at a quarter beat each but `{ooo}` would play three snare hits at 3/8 beats each.

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

## Documentation

For more information on FoxDot, please see the `docs` folder or go to http://foxdot.org/index.php/documentation/ (although largely unwritten)

## Thanks

- The SuperCollider development community and, of course, James McCartney, its original developer
- PyOSC, Artem Baguinski et al
- Sounds in the `samples/kindohm` folder courtesy of Mike Hodnick's live coded album, [Expedition](https://github.com/kindohm/expedition)
