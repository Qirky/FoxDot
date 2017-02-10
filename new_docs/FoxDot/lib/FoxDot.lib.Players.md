# `FoxDot.lib.Players`

Copyright Ryan Kirkbride 2015

This module contains the objects for Instrument Players (those that send musical
information to SuperCollider) and Sample Players (those that send buffer IDs to
playback specific samples located in the Samples directory).

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

##### `now(self, attr=degree, x=0)`

Calculates the values for each attr to send to the server at the current clock time 

##### `stutter(self, n=2, **kwargs)`

Plays the current note n-1 times over the current durations 

##### `reverse(self)`

Sets flag to reverse streams 

##### `offbeat(self, dur=0.5)`

Off sets the next event occurence 

##### `degrade(self, amount=0.5)`

Sets the amp modifier to a random array of 0s and 1s
amount=0.5 weights the array to equal numbers 

##### `largest_attribute(self)`

Returns the length of the largest nested tuple in the attr dict 

##### `f(self, *data)`

adds value to frequency modifier 

##### `bang(self, **kwargs)`

Triggered when sendNote is called. Responsible for any
action to be triggered by a note being played. Default action
is underline the player

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `__sub__(self, data)`

Change the degree modifier stream 

##### `get_event(self)`

Returns a dictionary of attr -> now values 

##### `__mul__(self, data)`

Multiplying an instrument player multiplies each amp value by
the input, or circularly if the input is a list. The input is
stored here and calculated at the update stage 

##### `num_key_references(self)`

Returns the number of 'references' for the
attr which references the most other players 

##### `osc_message(self, index=0, **kwargs)`

NEW: Creates an OSC packet to play a SynthDef in SuperCollider,
use kwargs to force values in the packet, e.g. pan=1 will force ['pan', 1] 

##### `strum(self, dur=0.025)`

Adds a delay to a Synth Envelope 

##### `stop(self, N=0)`

Removes the player from the Tempo clock and changes its internal
playing state to False in N bars time
- When N is 0 it stops immediately

##### `kill(self)`

Removes this object from the Clock and resets itself

##### `whenmod(self, mod, n, cmd, *args, **kwargs)`

Every n beats, do self.cmd(args) 

##### `every(self, n, cmd, *args, **kwargs)`

Every n beats, do self.cmd(args) 

##### `calculate_freq(self)`

Uses the scale, octave, and degree to calculate the frequency values to send to SuperCollider 

##### `follow(self, lead, follow=True)`

Takes a now object and then follows the notes 

##### `send(self, **kwargs)`

Sends the current event data to SuperCollder.
Use kwargs to overide values in the 

##### `__add__(self, data)`

Change the degree modifier stream 

##### `shuffle(self)`

Shuffles the degree of a player. If possible, do it visually 

---

### `PlayerKey(self, value=None, reference=None)`



#### Methods

---

### `func_delay(self, func, *args, **kwargs)`



#### Methods

---

### `send_delay(self, p, synthdef, message, fx={})`

Holds the state of a player whose send has
been scheduled in the future 

#### Methods

---

## Functions

## Data

