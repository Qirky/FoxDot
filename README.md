FoxDot - Live Coding with Python v0.3.2
=======================================

FoxDot is a Python programming environment that provides a fast and user-friendly abstraction to SuperCollider. It also comes with its own IDE, which means it can be used straight out of the box; all you need is Python and SuperCollider and you're ready to go!

### v0.3.2 fixes and updates

- `PlayerKey` data type can handle `PGroup` transformations without crashing, which improves performance when using `follow`
- `PlayerKey` data type greater than and less than functions fixed and now works with amplitudes.
- Better handling of scheduled functions that are "late"
- Experimental: `play` SynthDef can have a rate of -1 to be played in reverse and also uses a keyword `coarse` similar in function to `chop`
- Added `Pattern` method, palindrome that appends a mirrored version of the pattern to itself.
- Removed visual feedback for shuffling, rotating, etc patterns in Players as it did not work correctly with nested patterns.

### Known bugs

- Using as `linvar` as the Clock tempo will crash the Clock.

See `docs/changelog` for more

---

## Installation and startup

#### Prerequisites
- [Python 2.7](https://www.python.org/downloads/release/python-2712/) - make sure you say "yes" if you'd like to add Python to your path.
- [SuperCollider 3.6 and above](http://supercollider.github.io/download)

#### Recommended
- [sc3 plugins](http://sc3-plugins.sourceforge.net/)

#### Installing FoxDot

- Open up a command prompt and type `pip install FoxDot`. This will download and install the latest stable version of FoxDot from the Python Package Index if you have properly configured Python.
- You can update FoxDot to the latest version if it's already installed by adding `-U` or `--upgrade` flag to this command.
- Alternatively, you can build from source from directly from this repository:
``` bash
$ git clone https://github.com/Qirky/FoxDot.git
$ cd FoxDot
$ python setup.py install
```
- Open SuperCollder and install the FoxDot Quark (this allows FoxDot to communicate with SuperCollider) by entering the following and pressing `Ctrl+Return` (this evaluates a line of code):
```supercollider
Quarks.install("https://github.com/Qirky/FoxDotQuark.git")
```
- Install the `BatLib` quark in SuperCollider by evaluating `include("BatLib")` in SuperCollider - this is required for the FoxDot Quark to run correctly (Requires [Git to be installed](http://git-scm.com/) on your machine if it is not already).
- Recompile the SuperCollider class library by going to `Language -> Recompile Class Library` or pressing `Ctrl+Shift+L` 

#### Startup

1. Open SuperCollider and type in `FoxDot.start` and evaluate this line. SuperCollider is now listening for messages from FoxDot. 
2. Start FoxDot by entering `python -m FoxDot` at the command line.
3. If you have installed the SC3 Plugins, use the "Code" drop-down menu to select "Use SC3 Plugins". Restart FoxDot and you'll have access to classes found in the SC3 Plugins.

#### Troubleshooting

##### Buffer mismatch error
If you are getting an error similar to "Buffer UGen channel mismatch: expected 2, yet buffer has 1 channels" in SuperCollider this just means that a mono audio file is being played back where SuperCollider was expecting stereo. Nothing to worry about!

##### `Decimator` class not defined
This is a class that is found in the SC3 plugins (link at the top) but if you don't have it installed, go to `lib/Settings/conf.py` and set `SC3_PLUGINS` to `False`.

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
p1 >> pads([0,1,2,3], dur=[1/4,3/4], sus=1, vib=4, scale=Scale.minor)
```

The keyword arguments `dur`, `oct`, and `scale` apply to all player objects - any others, such as `vib` in the above example, refer to keyword arguments in the corresponding `SynthDef`. The first argument, `degree`, does not have to be stated explicitly. Notes can be grouped together so that they are played simultaneously using round brackets, `()`. The sequence `[(0,2,4),1,2,3]` will play the the the first harmonic triad of the default scale followed by the next three notes. 

### 'Sample Player' Objects

In FoxDot, sound files can be played through using a specific SynthDef called `play`. A player object that uses this SynthDef is referred to as a Sample Player object. Instead of specifying a list of numbers to generate notes, the Sample Player takes a string of characters (known as a "PlayString") as its first argument. To see a list of what samples are associated to what characters, use `print Samples`. To create a basic drum beat, you can execute the following line of code:

``` python
d1 >> play("x-o-")
```

To have samples play simultaneously, just create a new 'Sample Player' object for some more complex patterns.

``` python
bd >> play("x( x)  ")
hh >> play("---[--]")
sn >> play("  o ")
```

**New in v0.2.3:** You can merge multiple PlayStrings together by using the `PZip` pattern:

``` python
d1 >> play( PZip("x( x)  ", "--[--]", "  o( [ o])") )
```

Grouping characters in round brackets laces the pattern so that on each play through of the sequence of samples, the next character in the group's sample is played. The sequence `(xo)---` would be played back as if it were entered `x---o---`. Using square brackets will force the enclosed samples to played in the same time span as a single character e.g. `--[--]` will play two hi-hat hits at a half beat then two at a quarter beat. You can play a random sample from a selection by using curly braces in your Play String like so:

``` python
d1 >> play("x-o{-[--]o[-o]}")
```

## Scheduling Player methods

You can perform actions like shuffle, mirror, and rotate on Player Objects just by calling the appropriate method.

```python
bd >> play("x o  xo ")

# Shuffle the contents of bd
bd.shuffle()
```

You can schedule these methods by calling the `every` method, which takes a list of durations (in beats), the name of the method as a string, and any other arguments. The following syntax mirrors the string of sample characters after 6 beats, then again 2 beats  later and also shuffles it every 8 beats. 

```python
bd >> play("x-o-[xx]-o(-[oo])").every([6,2], 'mirror').every(8, 'shuffle')
```

## Player Object Keywords

dur - Durations (defaults to 1 and 1/2 for the Sample Player)

sus - Sustain (defaults to `dur`)

amp - Amplitude (defaults to 1)

pan - Panning, where -1 is far left, 1 is far right (defaults to 0)

vib - Vibrato (defaults to 0)

hpf - High-pass filter; only frequences **above** this value are kept in the final signal (defaults to 0)

lpf - Low-pass filter; only frequences **below** this value are kept in final signal (defaults to 20000)

bits - The bit depth that the signal is reduced to; this is a value between 1 and 24 where other values are ignored (defaults to 0)

rate - Variable keyword used for misc. changes to a signal. E.g. Playback rate of the Sample Player (defaults to 1)

verb - The dry/wet mix of reverb; this should be a value between 0 and 1 (defalts to 0.25)

room - Room size for reverb; this should be a value between 0 and 1 (defaults, to 0)

chop -'Chops' the signal into smaller chunks (defaults to 0)

delay - A duration of time to wait before sending the information to SuperCollider (defaults to 0)

slide - 'Slides' the frequency value of a signal to `freq * (slide+1)` over the  duration of a note (defaults to 0)

echo - Sets the decay time for any echo effect in beats, works best on Sample Player (defaults to 0)

sample - Special keyword for Sample Players; selects another audio file from the bank of samples for a sample character.

## Documentation

For more information on FoxDot, please see the `docs` folder or go to http://foxdot.org/index.php/documentation/ (although largely unwritten)

## Thanks

- The SuperCollider development community and, of course, James McCartney, its original developer
- PyOSC, Artem Baguinski et al
- Members of the Live Coding community who have contributed to the project in one way or another including, but not limited to, Alex McLean, Sean Cotterill, and Dan Hett.
- Big thanks to those who have used, tested, and submitted bugs, which have all helped improve FoxDot

### Samples

FoxDot's audio files have been obtained from a number of sources but I've lost record of which files are attributed to which original author. Here's a list of thanks for the unknowing creators of FoxDot's sample archive. 

- [Legowelt Sample Kits](https://awolfe.home.xs4all.nl/samples.html)
- [Game Boy Drum Kit](http://bedroomproducersblog.com/2015/04/08/game-boy-drum-kit/)
- A number of sounds courtesy of Mike Hodnick's live coded album, [Expedition](https://github.com/kindohm/expedition)
- Many samples have been obtained from http://freesound.org and have been placed in the public domain via the Creative Commons 0 License: http://creativecommons.org/publicdomain/zero/1.0/ - thank you to the original creators
- Other samples have come from the [Dirt Sample Engine](https://github.com/tidalcycles/Dirt-Samples/tree/c2db9a0dc4ffb911febc613cdb9726cae5175223) which is part of the TidalCycles live coding language created by Yaxu - another huge amount of thanks.
