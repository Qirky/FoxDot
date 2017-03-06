# `FoxDot.lib.Players`

Making music with FoxDot Players
--------------------------------

Players are what make FoxDot make music. They are similar in design to
SuperCollider's `PDef` and `PBind` combo but with slicker syntax. FoxDot
uses SuperCollider to *actually* make the sound and does so by triggering
predefined `SynthDefs` - sort of like definitions of a digital instruments.
To have a look at the list of `SynthDefs`, you can just `print` them to
the console:

```python
print SynthDefs
```

Each one of these represents a `SynthDef` *object*. These objects are then
given to Players to play - like giving an instrument to someone in your
orchestra. To give someone the instrument, `pads`, you use a double arrow
some code syntax like this:

```python
p1 >> pads()
```

`p1` is the name of a predefined player object. At startup, FoxDot reserves
all one- and two-character variable names, such as `x`, `p1`, or `bd` for
player objects but these can be repurposed if you like. If you want to use
a variable name for a player object with more than two characters, you just
instantiate a new `Player` object:

```python
new_player = Player()

new_player >> pads()
```

Changing parameters
-------------------

By default, player objects play the first note of their default scale (more
below) with a duration of 1 beat per note. To change the pitch just give the
`SynthDef` a list of numbers.

```python
p1 >> pads([0,7,6,4])
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

# Change the tempo
Clock.bpm = 144
```

To change the rhythm of your player object, specify the durations using
the `dur` keyword. Other keywords can be specified, such as `oct` for the
octave and `sus` for the sustain, which is the same as the duration by
default.

```python
p1 >> pads([0,7,6,4], dur=[1,1/2,1/4,1/4], oct=6, sus=1)

# See a list of possible keyword arguments
print Player.Attributes()
```

Using the `play` SynthDef
-------------------------

There is a special case SynthDef object called `play` which allows you
to play short audio files rather than specify pitches. In this case
you use a string of characters as the first argument where each character
refers to a different folder of audio files. You can see more information
by evaluating `print BufferManager`. The following line of code creates
a basic drum beat:

```python
d1 >> play("x-o-")
```

To play multiple patters simultaneously, just create a new `play` object.

```python
bd >> play("x( x)  ")
hh >> play("---[--]")
sn >> play("  o ")
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

## Classes

### `Group(self, *args)`



#### Methods

##### `__getattr__(self, name)`

Returns a Pattern object containing the desired attribute for each player in the group  

---

### `GroupAttr(self)`



#### Methods

---

### `Player(self)`



#### Methods

##### `__add__(self, data)`

Change the degree modifier stream 

##### `__mul__(self, data)`

Multiplying an instrument player multiplies each amp value by
the input, or circularly if the input is a list. The input is
stored here and calculated at the update stage 

##### `__rshift__(self, other)`

The PlayerObject Method >> 

##### `__sub__(self, data)`

Change the degree modifier stream 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `bang(self, **kwargs)`

Triggered when sendNote is called. Responsible for any
action to be triggered by a note being played. Default action
is underline the player

##### `calculate_freq(self)`

Uses the scale, octave, and degree to calculate the frequency values to send to SuperCollider 

##### `degrade(self, amount=0.5)`

Sets the amp modifier to a random array of 0s and 1s
amount=0.5 weights the array to equal numbers 

##### `every(self, n, cmd, *args, **kwargs)`

Every n beats, do self.cmd(args) 

##### `f(self, *data)`

adds value to frequency modifier 

##### `follow(self, lead, follow=True)`

Takes a now object and then follows the notes 

##### `get_event(self)`

Returns a dictionary of attr -> now values 

##### `kill(self)`

Removes this object from the Clock and resets itself

##### `largest_attribute(self)`

Returns the length of the largest nested tuple in the attr dict 

##### `now(self, attr=degree, x=0)`

Calculates the values for each attr to send to the server at the current clock time 

##### `num_key_references(self)`

Returns the number of 'references' for the
attr which references the most other players 

##### `offbeat(self, dur=0.5)`

Off sets the next event occurence 

##### `osc_message(self, index=0, **kwargs)`

NEW: Creates an OSC packet to play a SynthDef in SuperCollider,
use kwargs to force values in the packet, e.g. pan=1 will force ['pan', 1] 

##### `reverse(self)`

Sets flag to reverse streams 

##### `send(self, **kwargs)`

Sends the current event data to SuperCollder.
Use kwargs to overide values in the 

##### `shuffle(self)`

Shuffles the degree of a player. If possible, do it visually 

##### `stop(self, N=0)`

Removes the player from the Tempo clock and changes its internal
playing state to False in N bars time
- When N is 0 it stops immediately

##### `strum(self, dur=0.025)`

Adds a delay to a Synth Envelope 

##### `stutter(self, n=2, **kwargs)`

Plays the current note n-1 times. You can specify some keywords,
such as dur, sus, and rate. 

##### `whenmod(self, mod, n, cmd, *args, **kwargs)`

Every n beats, do self.cmd(args) 

---

### `PlayerKey(self, value=None, reference=None)`



#### Methods

---

### `func_delay(self, func, *args, **kwargs)`



#### Methods

---

### `rest(self, dur=1)`

Represents a rest when used with a Player's `dur` keyword
    

#### Methods

---

### `send_delay(self, p, synthdef, message, fx={})`

Holds the state of a player whose send has
been scheduled in the future 

#### Methods

---

## Functions

## Data

