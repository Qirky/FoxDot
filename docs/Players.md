# `Players`

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

##### `Attributes(cls)`

Returns a list of possible keyword arguments for FoxDot players and effects 

##### `__add__(self, data)`

Change the degree modifier stream 

##### `__call__(self, **kwargs)`

Sends the next osc message to SuperCollider and schedules the
next event for this player 

##### `__rshift__(self, other)`

Handles the allocation of SynthDef objects using >> syntax 

##### `__sub__(self, data)`

Change the degree modifier stream 

##### `accompany(self, other, values=[0, 2, 4], debug=False)`

Similar to "follow" but when the value has changed 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in 'n' beats time
```
# Stop the player looping after 16 beats
p1 >> pads().after(16, "stop")
```

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

##### `dur_updated(self)`

Returns True if the players duration has changed since the last call 

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

##### `lshift(self, n=1)`

Plays the event behind 

##### `map(self, key1, key2, mapping)`

Sets the attribute for self.key2 to self.key1
altered with a mapping dictionary.

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

##### `only(self)`

Stops all players except this one 

##### `osc_message(self, index=0, **kwargs)`

Creates an OSC packet to play a SynthDef in SuperCollider,
use kwargs to force values in the packet, e.g. pan=1 will force ['pan', 1] 

##### `reset(self)`

Sets all Player attributes to 0 unless their default is specified by an effect 

##### `reverse(self)`

Reverses every attribute stream 

##### `rhythm(self)`

Returns the "now" value of the duration 

##### `rotate(self, n=1)`

Rotates the values in the degree by 'n' 

##### `rshift(self, n=1)`

Plays the event in front 

##### `send(self, **kwargs)`

Sends the current event data to SuperCollder.
Use kwargs to overide values in the current event 

##### `shuffle(self)`

Shuffles the degree of a player. 

##### `smap(self, kwargs)`

Like map but maps the degree to the sample attribute
        

##### `solo(self, action=1)`

Silences all players except this player. Undo the silence
by using `Player.solo(0)` 

##### `spread(self, on=1)`

Sets pan to (-1, 1) and pshift to (0, 0.125)

##### `stop(self, N=0)`

Removes the player from the Tempo clock and changes its internal
playing state to False in N bars time
- When N is 0 it stops immediately

##### `strum(self, dur=0.025)`

Adds a delay to a Synth Envelope 

##### `stutter(self, n=2, **kwargs)`

Plays the current note n-1 times. You can specify keywords. 

##### `unpack(self, item, debug=False)`

Converts a pgroup to floating point values and updates and time var or playerkey relations 

##### `update(self, synthdef, degree, **kwargs)`

Updates the attributes of the player. Called using the >> syntax.
        

##### `update_player_key(self, key, value, time)`

Forces object's dict uses PlayerKey instances
        

##### `versus(self, other, key=<lambda>, f=<built-in function max>)`

Takes another Player object and a function that takes
two player arguments and returns one, default is the higher
pitched

---

### `rest(self, dur=1)`

Represents a rest when used with a Player's `dur` keyword
    

#### Methods

---

## Functions

## Data

