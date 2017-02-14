FoxDot - Live Coding with Python v0.2.7
=======================================

*FoxDot is a pre-processed Python programming environment that provides a fast and user-friendly abstraction to SuperCollider. It also comes with its own IDE, which means it can be used straight out of the box; all you need is Python and SuperCollider and you're ready to go!*

### v0.2.7 fixes and updates

- Rest class added
- Undo and Redo functions fixed
- Infinite loop caused by empty brackets in PlayStrings fixed
- Menu bar added with several short-cuts
- Player follow method improved
- Improved documentation
- "style" keyword argument changed to "sample"

See `docs/changelog` for more

---

## Installation and startup

#### Prerequisites
- [Python 2.7](https://www.python.org/downloads/release/python-2712/)
- [SuperCollider 3.6 and above](http://supercollider.github.io/download)

#### Recommended
- [sc3 plugins](http://sc3-plugins.sourceforge.net/)

#### Installing FoxDot

- Install the latest version from the Python Package Index from the command line by executing `pip install FoxDot`
- Alternatively, you can build from source:
``` bash
git clone https://github.com/Qirky/FoxDot.git
cd FoxDot
python setup.py install
```
- Open SuperCollder and install the FoxDot Quark (this allows FoxDot to communicate with SuperCollider) by entering the following and pressing `Ctrl+Return` (this evaluates a line of code):
```supercollider
Quarks.install("https://github.com/Qirky/FoxDotQuark.git")
```
- Recompile the SuperCollider class library by going to `Language -> Recompile Class Library` or pressing `Ctrl+Shift+L`

#### Startup

1. Open SuperCollider and type in `FoxDot.start` and evaluate this line. SuperCollider is now listening for messages from FoxDot. 
2. Start FoxDot by entering `python -m FoxDot` at the command line.

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

Assigning synths and instructions to a player object is done using the double-arrow operator `>>`. So if you wanted to assign a synth to `p1` called 'pads' (execute `print Synths` to see all available synths) you would use the following code:

``` python
p1 >> pads([0,1,2,3])
```

The empty player object, `p1` is now assigned a the 'pads' synth and some playback instructions. `p1` will play the first four notes of the default scale using a SuperCollider `SynthDef` with the name `\pads`. By default, each note lasts for 1 beat at 120 bpm. These defaults can be changed by specifying keyword arguments:

``` python
p1 >> pads([0,1,2,3], dur=[1/4,3/4], sus=1, vib=4, scale=Scale.minor)
```

The keyword arguments `dur`, `oct`, and `scale` apply to all player objects - any others, such as `vib` in the above example, refer to keyword arguments in the corresponding `SynthDef`. The first argument, `degree`, does not have to be stated explicitly. Notes can be grouped together so that they are played simultaneously using round brackets, `()`. The sequence `[(0,2,4),1,2,3]` will play the the the first harmonic triad of the default scale followed by the next three notes. 

### 'Sample Player' Objects

In FoxDot, sound files can be played through using a specific SynthDef called `play`. A player object that uses this SynthDef is referred to as a Sample Player object. Instead of specifying a list of numbers to generate notes, the Sample Player takes a string of characters (known as a "PlayString") as its first argument. Each character in the string refers to one sample (the current list can be seen in the `FoxDot/lib/Settings/samplelib.csv` file, which you can customise if you so wish). To create a basic drum beat, you can execute the following line of code:

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

room - Room size for reverb; this should be a value between 0 and 1 (defaults, to 0.3)

chop -'Chops' the signal into smaller chunks (defaults to 0)

delay - A duration of time to wait before sending the information to SuperCollider (defaults to 0)

slide - 'Slides' the frequency value of a signal to `freq * (slide+1)` over the  duration of a note (defaults to 0)

echo - Sets the decay time for any echo effect in beats, works best on Sample Player (defaults to 0)

scrub - Special keyword for Sample Players; changes the playback rate to change like a DJ scratching a record (defaults to 0)

sample - Special keyword for Sample Players; selects another audio file for a sample character.

## Documentation

For more information on FoxDot, please see the `docs` folder or go to http://foxdot.org/index.php/documentation/ (although largely unwritten)

## Thanks

- The SuperCollider development community and, of course, James McCartney, its original developer
- PyOSC, Artem Baguinski et al
- Sounds in `snd/z/` folder courtesy of Mike Hodnick's live coded album, [Expedition](https://github.com/kindohm/expedition)
- Many samples have been obtained from http://freesound.org and have been placed in the public domain via the Creative Commons 0 License: http://creativecommons.org/publicdomain/zero/1.0/ - thank you to the original creators
- Other samples have come from the [Dirt Sample Engine](https://github.com/tidalcycles/Dirt-Samples/tree/c2db9a0dc4ffb911febc613cdb9726cae5175223) which is part of the TidalCycles live coding language created by Yaxu - another huge amount of thanks.
