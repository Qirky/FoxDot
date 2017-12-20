# `Players`

Players are what make FoxDot make music. They are similar in design to
SuperCollider's `PDef` and `PBind` combo but with slicker syntax. FoxDot
uses SuperCollider to *actually* make the sound and does so by triggering
predefined `SynthDefs` - sort of like definitions of a digital instruments.
To have a look at the list of `SynthDefs`, you can just `print` them to
the console:

```python
print(SynthDefs)
```

Each one of these represents a `SynthDef` *object*. These objects are then
given to Players to play - like giving an instrument to someone in your
orchestra. To give someone the instrument, `pads`, you use a double arrow
some code syntax like this:

```python
p1 >> pads()
```

To stop a Player, use the `stop` method e.g. `p1.stop()`. If you want to
stop all players, you can use the command `Clock.clear()` or the keyboard
shortcut `Ctrl+.`, which executes this command.

`p1` is the name of a predefined player object. At startup, FoxDot reserves
all one- and two-character variable names, such as `x`, `p1`, or `bd` for
player objects but these can be repurposed if you like. If you want to use
a variable name for a player object with more than two characters, you just
instantiate a new `Player` object:

```python
foo = Player()

foo >> pads()
```

Changing parameters
-------------------

By default, player objects play the first note of their default scale (more
below) with a duration of 1 beat per note. To change the pitch just give the
`SynthDef` a list of numbers.

```python
p1 >> pads([0,7,6,4])
```

Play multiple pitches together by putting them in round brackets:

```python
p1 >> pads([0,2,4,(0,2,4)])
```

When you start FoxDot up, your clock is ticking at 120bpm and your player
objects are all playing in the major scale. With 8 pitches in the major scale,
the 0 refers to the first pitch and the 7 refers to the pitch one octave
higher because Python, like most programming languages, uses zero-indexing.
To change your scale you can specify a new scale as a keyword argument (see
the documentation on `Scales` for more information on scales) or change the
default scale for all player objects.

```python
# Changing scale as a keyword argument
p1 >> pads([0,7,6,4], scale=Scale.minor)

# Changing the default scalew (the following are equivalent)
Scale.default.set("minor")
Scale.default.set(Scale.minor)
Scale.default.set([0,2,3,5,7,8,10])

# See a list of scales
print Scale.names()

# Change the tempo (this takes effect at the next bar)
Clock.bpm = 144
```

To change the rhythm of your player object, specify the durations using
the `dur` keyword. Other keywords can be specified, such as `oct` for the
octave and `sus` for the sustain, which is the same as the duration by
default.

```python
p1 >> pads([0,7,6,4], dur=[1,1/2,1/4,1/4], oct=6, sus=1)

# See a list of possible keyword arguments
print(Player.get_attributes())
```

Using the `play` SynthDef
-------------------------

There is a special case SynthDef object called `play` which allows you
to play short audio files rather than specify pitches. In this case
you use a string of characters as the first argument where each character
refers to a different folder of audio files. You can see more information
by evaluating `print(Samples)`. The following line of code creates
a basic drum beat:

```python
d1 >> play("x-o-")
```

To play multiple patterns simultaneously, you can create a new `play` object. This
is useful if you want to have different attributes for each player.

```python
bd >> play("x( x)  ", dur=1)
hh >> play("---[--]", dur=[1/2,1/2,1/4], rate=4)
sn >> play("  o ", rate=(.9,1), pan=(-1,1))
```    

Grouping characters in round brackets laces the pattern so that on each
play through of the sequence of samples, the next character in the group's
sample is played. The sequence `(xo)---` would be played back as if it
were entered `x---o---`. Using square brackets will force the enclosed samples
to played in the same time span as a single character e.g. `--[--]` will play
two hi-hat hits at a half beat then two at a quarter beat. You can play a
random sample from a selection by using curly braces in your Play String
like so:

```
d1 >> play("x-o{-[--]o[-o]}")
```

FoxDot Player Object Keywords
-----------------------------

dur - Durations (defaults to 1 and 1/2 for the Sample Player)

sus - Sustain (defaults to `dur`)

amp - Amplitude (defaults to 1)

rate - Variable keyword used for misc. changes to a signal. E.g. Playback rate of the Sample Player (defaults to 1)

delay - A duration of time to wait before sending the information to SuperCollider (defaults to 0)

sample - Special keyword for Sample Players; selects another audio file from the bank of samples for a sample character.

## Classes

### `Group(self, *args)`



#### Methods

---

### `GroupAttr(self, *args, **kwargs)`

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

#### Methods

---

### `Player(self, name=None)`

FoxDot generates music by creating instances of `Player` and giving them instructions
to follow. At startup FoxDot creates many instances of `Player` and assigns them to
any valid two character variable. This is so that when you start playing you don't 
have to worry about typing `myPlayer = Player()` and `myPlayer_2 = Player()` every
time you want to do something new. Of course there is nothing stopping you from 
doing that if yo so wish.

Instances of `Player` are given instructions to generate music using the `>>` syntax,
overriding the bitshift operator, and should be given an instance of `SynthDefProxy`.
A `SynthDefProxy` is created when calling an instance of `SynthDef` - these are the
"instruments" used by player objects and are written in SuperCollider code. You can
see more information about these in the `SCLang` module. Below describes how to assign
a `SynthDefProxy` of the `SynthDef` `pads` to a `Player` instance called `p1`:

```python
# Calling pads as if it were a function returns a 
# pads SynthDefProxy object which is assigned to p1
p1 >> pads()

# You could store several instances and assign them at different times
proxy_1 = pads([0,1,2,3], dur=1/2)
proxy_2 = pads([4,5,6,7], dur=1)

p1 >> proxy_1 # Assign the first to p1
p1 >> proxy_2 # This replaces the instructions being followed by p1
```

#### Methods

##### `Attributes(cls)`

To be replaced by `Player.get_attributes()` 

##### `get_attributes(cls)`

Returns a list of possible keyword arguments for FoxDot players and effects 

---

### `PlayerKeyException(self, *args, **kwargs)`

Common base class for all non-exit exceptions.

#### Methods

---

### `rest(self, dur=1)`

Represents a rest when used with a Player's `dur` keyword
    

#### Methods

---

## Functions

## Data

