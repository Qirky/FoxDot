FoxDot - Live Coding with Python v0.8
=====================================

## Please note

I will not be actively maintaining FoxDot until January 2020 and will not be making changes to the code in response to issues / pull requests in this time. However, you can still ask questions on the [TOPLAP FoxDot Forum](https://forum.toplap.org/c/communities/foxdot) and I will get back to you when I can. Please do not ask general questions in the "issues" section. Thanks.

---

FoxDot is a Python programming environment that provides a fast and user-friendly abstraction to SuperCollider. It also comes with its own IDE, which means it can be used straight out of the box; all you need is Python and SuperCollider and you're ready to go!

## Important

If you are having trouble installing using `pip install FoxDot`, try updating Python's `setuptools` and `wheel` libraries using the following code and trying again.

```
pip install -U setuptools
pip install -U wheel
```

### v0.8 Updates

- Added `stretch` synth for timestretching samples, similar to `loop` but better and only plays the whole file. Stretches the audio's duration to the `sus` attribute without affecting pitch and does not require the tempo to be known.

```python
# Stretches the audio to 4 beats without affecting pitch
p1 >> stretch("Basic_Rock_135", dur=4)
```

---

## Installation and startup

#### Prerequisites
- [Python 2 or 3](https://www.python.org/) - add Python to your path and install "pip" when prompted during the install.
- [SuperCollider 3.8 and above](http://supercollider.github.io/download)

#### Recommended
- [sc3 plugins](http://sc3-plugins.sourceforge.net/)

#### Installing FoxDot

- Open up a command prompt and type `pip install --user FoxDot`. This will download and install the latest stable version of FoxDot from the Python Package Index if you have properly configured Python.
- You can update FoxDot to the latest version if it's already installed by adding `-U` or `--upgrade` flag to this command.
- Alternatively, you can build from source from directly from this repository:
``` bash
$ git clone https://github.com/Qirky/FoxDot.git
$ cd FoxDot
$ python setup.py install
```
- Open SuperCollder and install the FoxDot Quark and its dependencies (this allows FoxDot to communicate with SuperCollider) by entering the following and pressing `Ctrl+Return` (Note: this requires [Git to be installed](http://git-scm.com/) on your machine if it is not already):
```supercollider
Quarks.install("FoxDot")
```
- Recompile the SuperCollider class library by going to `Language -> Recompile Class Library` or pressing `Ctrl+Shift+L` 

#### Startup

1. Open SuperCollider and type in `FoxDot.start` and evaluate this line. SuperCollider is now listening for messages from FoxDot. 
2. Start FoxDot by entering `FoxDot` at the command line. If that doesn't work, try `python -m FoxDot`.
3. If you have installed the SC3 Plugins, use the "Code" drop-down menu to select "Use SC3 Plugins". Restart FoxDot and you'll have access to classes found in the SC3 Plugins.
4. Keep up to date with the latest verion of FoxDot by running `pip install FoxDot --upgrade` every few weeks.
5. Check out the [YouTube tutorials](https://www.youtube.com/channel/UCRyrNX07lFcfRSymZEWwl6w) for some in-depth tutorial videos on getting to grips with FoxDot

#### Installing with SuperCollider 3.7 or earlier

If you are having trouble installing the FoxDot Quark in SuperCollider, it is usually because the version of SuperCollider you are installing doesn’t have the functionality for installing Quarks or it doesn’t work properly. If this is the case, you can download the contents of the following SuperCollider script: [foxdot.scd](http://foxdot.org/wp-content/uploads/foxdot.scd). Once downloaded, open the file in SuperCollider and press Ctrl+Return to run it. This will make SuperCollider start listening for messages from FoxDot.

#### Frequently Asked Questions

You can find answers to many frequently asked questions on the [FAQ post on the FoxDot discussion forum](http://foxdot.org/forum/?view=thread&id=1).

## Basics

### Executing Code

A 'block' of code in FoxDot is made up of consecutive lines of code with no empty lines. Pressing `Ctrl+Return` (or `Cmd+Return` on a Mac) will execute the block of code that the cursor is currently in. Try `print(1 + 1)` to see what happens!

### Player Objects

Python supports many different programming paradigms, including procedural and functional, but FoxDot implements a traditional object orientated approach with a little bit of cheating to make it easier to live code. A player object is what FoxDot uses to make music by assigning it a synth (the 'instrument' it will play) and some instructions, such as note pitches. All one and two character variable names are reserved for player objects at startup so, by default, the variables `a`, `bd`, and `p1` are 'empty' player objects. If you use one of these variables to store something else but want to use it as a player object again, or you  want to use a variable with more than two characters, you just have to reserve it by creating a `Player` and assigning it like so:

``` python
p1 = Player("p1") # The string name is optional
```

To stop a Player, use the `stop` method e.g. `p1.stop()`. If you want to stop all players, you can use the command `Clock.clear()` or the keyboard short-cut `Ctrl+.`, which executes this command.

Assigning synths and instructions to a player object is done using the double-arrow operator `>>`. So if you wanted to assign a synth to `p1` called 'pads' (execute `print(SynthDefs)` to see all available synths) you would use the following code:

``` python
p1 >> pads([0,1,2,3])
```

The empty player object, `p1` is now assigned a the 'pads' synth and some playback instructions. `p1` will play the first four notes of the default scale using a SuperCollider `SynthDef` with the name `\pads`. By default, each note lasts for 1 beat at 120 bpm. These defaults can be changed by specifying keyword arguments:

```python
p1 >> pads([0,1,2,3], dur=[1/4,3/4], sus=1, vib=4, scale=Scale.minor)
```

The keyword arguments `dur`, `oct`, and `scale` apply to all player objects - any others, such as `vib` in the above example, refer to keyword arguments in the corresponding `SynthDef`. The first argument, `degree`, does not have to be stated explicitly. Notes can be grouped together so that they are played simultaneously using round brackets, `()`. The sequence `[(0,2,4),1,2,3]` will play the the the first harmonic triad of the default scale followed by the next three notes. 

### 'Sample Player' Objects

In FoxDot, sound files can be played through using a specific SynthDef called `play`. A player object that uses this SynthDef is referred to as a Sample Player object. Instead of specifying a list of numbers to generate notes, the Sample Player takes a string of characters (known as a "PlayString") as its first argument. To see a list of what samples are associated to what characters, use `print(Samples)`. To create a basic drum beat, you can execute the following line of code:

``` python
d1 >> play("x-o-")
```

To have samples play simultaneously, you can create a new 'Sample Player' object for some more complex patterns.

``` python
bd >> play("x( x)  ")
hh >> play("---[--]")
sn >> play("  o ")
```

Alternatively, you can do this in one line using `<>` arrows to separate patterns you want to play together like so:

```python
d1 >> play("<x( x)  ><---[--]><  o >")
```

Or you can use `PZip`, the `zip` method, or the `&` sign to create one pattern that does this. This can be useful if you want to perform some function on individual layers later on:

``` python
d1 >> play(P["x( x)  "].palindrome().zip("---[--]").zip(P["  o "].amen()))  

# The first item must be a P[] pattern, not a string. 

d1 >> play(P["x( x)  "].palindrome() & "---[--]" & P["  o "].amen())
```

Grouping characters in round brackets laces the pattern so that on each play through of the sequence of samples, the next character in the group's sample is played. The sequence `(xo)---` would be played back as if it were entered `x---o---`. Using square brackets will force the enclosed samples to played in the same time span as a single character e.g. `--[--]` will play two hi-hat hits at a half beat then two at a quarter beat. You can play a random sample from a selection by using curly braces in your Play String like so:

``` python
d1 >> play("x-o{-[--]o[-o]}")
```

There is now the functionality to specify the sample number for an individual sample when using the `play` SynthDef. This can be done from the play string itself by using the bar character in the form `|<char><sample>|`. These can also be patterns created using brackets:

```python
# Plays the kick drum with sample 2 but the rest with sample 0
p1 >> play("|x2|-o-")

# You can use square brackets to play multiple samples
p1 >> play("|x[12]| o ")

# Round brackets alternate which sample is used on each loop through the sequence
p1 >> play("|x(12)| o ")

# Curly braces will pick a sample at random
p1 >> play("|x{0123}| o ")
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

## Documentation

[Link to documentation website](https://foxdot.org/docs/) (still in progress)

## Using alternative editors

FoxDot comes pre-packaged with its own basic editor so that you don't have to tinker with config files or download any other tools but if you want to use an existing editor you can. [Koltes](https://github.com/KoltesDigital) has written a plugin for the popular Atom editor. You can install it by going to Settings -> Install -> Searching "foxdot" and pressing install on the plug in. Press Ctrl+Alt+f or go to menu -> Packages -> FoxDot  -> Toggle to start FoxDot running.

## Running Python files with FoxDot code

You can import `FoxDot` into your own Python programs as you would any other module. If you are not writing an interactive program, i.e. only containing FoxDot code, then you need to call a function `Go()` at the end of your program to get playback otherwise the program will terminate immediately. For example your program, `my_file.py`, should look something like this:

```python
from FoxDot import *
p1 >> pads([0, 1, 2, 3])
d1 >> play("x-o-")
Go()
```

Then just run like any other Python program: `python my_file.py`

## Thanks

- The SuperCollider development community and, of course, James McCartney, its original developer
- PyOSC, Artem Baguinski et al
- Members of the Live Coding community who have contributed to the project in one way or another including, but not limited to, Alex McLean, Sean Cotterill, and Dan Hett.
- Big thanks to those who have used, tested, and submitted bugs, which have all helped improve FoxDot
- Thank you to those who have found solutions for SuperCollider related issues, such as DavidS48

### Samples

FoxDot's audio files have been obtained from a number of sources but I've lost record of which files are attributed to which original author. Here's a list of thanks for the unknowing creators of FoxDot's sample archive. 

- [Legowelt Sample Kits](https://awolfe.home.xs4all.nl/samples.html)
- [Game Boy Drum Kit](http://bedroomproducersblog.com/2015/04/08/game-boy-drum-kit/)
- A number of sounds courtesy of Mike Hodnick's live coded album, [Expedition](https://github.com/kindohm/expedition)
- Many samples have been obtained from http://freesound.org and have been placed in the public domain via the Creative Commons 0 License: http://creativecommons.org/publicdomain/zero/1.0/ - thank you to the original creators
- Other samples have come from the [Dirt Sample Engine](https://github.com/tidalcycles/Dirt-Samples/tree/c2db9a0dc4ffb911febc613cdb9726cae5175223) which is part of the TidalCycles live coding language created by Yaxu - another huge amount of thanks.

If you feel I've used a sample where I shouldn't have, please get in touch!
