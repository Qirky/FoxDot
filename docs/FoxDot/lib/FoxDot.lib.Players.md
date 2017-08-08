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

Play multiple pitches together by putting them in round brackets:

p1 >> pads([0,2,4,(0,2,4)])

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
print Player.Attributes()
```

Using the `play` SynthDef
-------------------------

There is a special case SynthDef object called `play` which allows you
to play short audio files rather than specify pitches. In this case
you use a string of characters as the first argument where each character
refers to a different folder of audio files. You can see more information
by evaluating `print Samples`. The following line of code creates
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

### `AccompanyKey(self, other, rel=[0, 2, 4])`

Like PlayerKey except it returns 

#### Methods

##### `__add__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__eq__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ge__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__gt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__le__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__lt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ne__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__pow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__radd__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rdiv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rpow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rsub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rtruediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rxor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__sub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__truediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__xor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `find_new_value(self, val)`

Finds the item in self.data that is closest to self.acmp_value 

##### `map(self, mapping)`

Creates a new Player key that maps the values in the dictionary (mapping)
to new values. Example use case:

```
d1 >> play("x-o-", sample=d1.degree.map( { "-" : -1, "o" : var([0,2]) }))
```

---

### `Group(self, *args)`



#### Methods

##### `__getattr__(self, name)`

Returns a Pattern object containing the desired attribute for each player in the group  

---

### `GroupAttr(self)`



#### Methods

---

### `NumberKey(self, value, reference)`



#### Methods

##### `__add__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__eq__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ge__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__gt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__le__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__lt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ne__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__pow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__radd__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rdiv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rpow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rsub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rtruediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rxor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__sub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__truediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__xor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `map(self, mapping)`

Creates a new Player key that maps the values in the dictionary (mapping)
to new values. Example use case:

```
d1 >> play("x-o-", sample=d1.degree.map( { "-" : -1, "o" : var([0,2]) }))
```

---

### `Player(self)`



#### Methods

##### `__add__(self, data)`

Change the degree modifier stream 

##### `__rshift__(self, other)`

Handles the allocation of SynthDef objects using >> syntax 

##### `__sub__(self, data)`

Change the degree modifier stream 

##### `accompany(self, other, values=[0, 2, 4])`

Similar to "follow" but when the value has changed 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `bang(self, **kwargs)`

Triggered when sendNote is called. Responsible for any
action to be triggered by a note being played. Default action
is underline the player

##### `count(self, time=None, event_after=False)`

Counts the number of events that will have taken place between 0 and `time`. If
`time` is not specified the function uses self.metro.now(). Setting `event_after`
to `True` will find the next event *after* `time`

##### `degrade(self, amount=0.5)`

Sets the amp modifier to a random array of 0s and 1s
amount=0.5 weights the array to equal numbers 

##### `every(self, n, cmd, *args, **kwargs)`

Every n beats, call a method (defined as a string) on the
object and use the args and kwargs. To call the method
every n-th beat of a timeframe, use the `cycle` keyword argument
to specify that timeframe.

```
# Call the shuffle method every 4 beats

p1.every(4, 'shuffle')

# Call the stutter method on the 5th beat of every 8 beat cycle

p1.every(5, 'stutter', 4, cycle=8)

```

##### `follow(self, lead=False)`

Takes a Player object and then follows the notes 

##### `get_event(self)`

Returns a dictionary of attr -> now values 

##### `kill(self)`

Removes this object from the Clock and resets itself

##### `largest_attribute(self, **kwargs)`

Returns the length of the largest nested tuple in the current event dict 

##### `mirror(self)`

The degree pattern is reversed 

##### `new_message(self, index=0, **kwargs)`

Returns the header of an osc message to be added to by osc_message() 

##### `now(self, attr=degree, x=0)`

Calculates the values for each attr to send to the server at the current clock time 

##### `num_key_references(self)`

Returns the number of 'references' for the
attr which references the most other players 

##### `number_attr(self, attr)`

Returns true if the attribute should be a number 

##### `number_of_layers(self, **kwargs)`

Returns the deepest nested item in the event 

##### `offbeat(self, dur=0.5)`

Off sets the next event occurence 

##### `osc_message(self, index=0, **kwargs)`

Creates an OSC packet to play a SynthDef in SuperCollider,
use kwargs to force values in the packet, e.g. pan=1 will force ['pan', 1] 

##### `reset(self)`

Sets all Player attributes to 0 unless their default is specified by an effect 

##### `reverse(self)`

Sets flag to reverse streams 

##### `rotate(self, n=1)`

Rotates the values in the degree by 'n' 

##### `send(self, **kwargs)`

Sends the current event data to SuperCollder.
Use kwargs to overide values in the current event 

##### `shuffle(self)`

Shuffles the degree of a player. 

##### `stop(self, N=0)`

Removes the player from the Tempo clock and changes its internal
playing state to False in N bars time
- When N is 0 it stops immediately

##### `strum(self, dur=0.025)`

Adds a delay to a Synth Envelope 

##### `stutter(self, n=2, **kwargs)`

Plays the current note n-1 times. You can specify keywords. 

##### `unpack(self, item)`

Converts a pgroup to floating point values and updates and time var or playerkey relations 

##### `update_player_key(self, key, value, time)`

Forces object's dict uses PlayerKey instances
        

##### `versus(self, other, key=<lambda>, f=<built-in function max>)`

Takes another Player object and a function that takes
two player arguments and returns one, default is the higher
pitched

---

### `PlayerKey(self, value=None, reference=None, parent=None, attr=None)`



#### Methods

##### `__add__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__eq__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ge__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__gt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__le__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__lt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ne__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__pow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__radd__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rdiv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rpow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rsub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rtruediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rxor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__sub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__truediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__xor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `map(self, mapping)`

Creates a new Player key that maps the values in the dictionary (mapping)
to new values. Example use case:

```
d1 >> play("x-o-", sample=d1.degree.map( { "-" : -1, "o" : var([0,2]) }))
```

---

### `rest(self, dur=1)`

Represents a rest when used with a Player's `dur` keyword
    

#### Methods

---

## Functions

## Data

