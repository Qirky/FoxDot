# `Players`

Players are what make FoxDot make music. They are similar in design to
SuperCollider's `PDef` and `PBind` combo but with slicker syntax. FoxDot
uses SuperCollider to *actually* make the sound and does so by triggering
predefined `SynthDefs` - sort of like definitions of a digital instruments.
To have a look at the list of `SynthDefs`, you can just `print` them to
the console: ::

    print(SynthDefs)

Each one of these represents a `SynthDef` *object*. These objects are then
given to Players to play - like giving an instrument to someone in your
orchestra. To give someone the instrument, `pads`, you use a double arrow
some code syntax like this: ::

    p1 >> pads()

To stop a Player, use the `stop` method e.g. `p1.stop()`. If you want to
stop all players, you can use the command `Clock.clear()` or the keyboard
shortcut `Ctrl+.`, which executes this command.

`p1` is the name of a predefined player object. At startup, FoxDot reserves
all one- and two-character variable names, such as `x`, `p1`, or `bd` for
player objects but these can be repurposed if you like. If you want to use
a variable name for a player object with more than two characters, you just
instantiate a new `Player` object: ::

    foo = Player()

    foo >> pads()

Changing parameters
-------------------

By default, player objects play the first note of their default scale (more
below) with a duration of 1 beat per note. To change the pitch just give the
`SynthDef` a list of numbers. ::

    p1 >> pads([0,7,6,4])

Play multiple pitches together by putting them in round brackets: ::

    p1 >> pads([0,2,4,(0,2,4)])

When you start FoxDot up, your clock is ticking at 120bpm and your player
objects are all playing in the major scale. With 8 pitches in the major scale,
the 0 refers to the first pitch and the 7 refers to the pitch one octave
higher because Python, like most programming languages, uses zero-indexing.
To change your scale you can specify a new scale as a keyword argument (see
the documentation on `Scales` for more information on scales) or change the
default scale for all player objects. ::

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

To change the rhythm of your player object, specify the durations using
the `dur` keyword. Other keywords can be specified, such as `oct` for the
octave and `sus` for the sustain, which is the same as the duration by
default. ::

    p1 >> pads([0,7,6,4], dur=[1,1/2,1/4,1/4], oct=6, sus=1)

    # See a list of possible keyword arguments
    print(Player.get_attributes())

Using the `play` SynthDef
-------------------------

There is a special case SynthDef object called `play` which allows you
to play short audio files rather than specify pitches. In this case
you use a string of characters as the first argument where each character
refers to a different folder of audio files. You can see more information
by evaluating `print(Samples)`. The following line of code creates
a basic drum beat: ::

    d1 >> play("x-o-")

To play multiple patterns simultaneously, you can create a new `play` object. This
is useful if you want to have different attributes for each player. ::
    
    bd >> play("x( x)  ", dur=1)
    hh >> play("---[--]", dur=[1/2,1/2,1/4], rate=4)
    sn >> play("  o ", rate=(.9,1), pan=(-1,1))

Grouping characters in round brackets laces the pattern so that on each
play through of the sequence of samples, the next character in the group's
sample is played. The sequence `(xo)---` would be played back as if it
were entered `x---o---`. Using square brackets will force the enclosed samples
to played in the same time span as a single character e.g. `--[--]` will play
two hi-hat hits at a half beat then two at a quarter beat. You can play a
random sample from a selection by using curly braces in your Play String
like so: ::

    d1 >> play("x-o{-[--]o[-o]}")

FoxDot Player Object Keywords
-----------------------------

dur - Durations (defaults to 1 and 1/2 for the Sample Player)

sus - Sustain (defaults to `dur`)

amp - Amplitude (defaults to 1)

rate - Variable keyword used for misc. changes to a signal. E.g. Playback rate of the Sample Player (defaults to 1)

delay - A duration of time to wait before sending the information to SuperCollider (defaults to 0)

sample - Special keyword for Sample Players; selects another audio file from the bank of samples for a sample character.

## Classes

### `EmptyPlayer(self, name)`

Place holder for Player objects created at run-time to reduce load time.
    

#### Methods

##### `__getattribute__(self, name)`

Tries to return the correct attr; if not init the Player and try again 

##### `__init__(self, name)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

##### `__rshift__(self, *args, **kwargs)`

Converts an EmptyPlayer to a Player. 

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
a `SynthDefProxy` of the `SynthDef` `pads` to a `Player` instance called `p1`: ::

    # Calling pads as if it were a function returns a 
    # pads SynthDefProxy object which is assigned to p1
    p1 >> pads()

    # You could store several instances and assign them at different times
    proxy_1 = pads([0,1,2,3], dur=1/2)
    proxy_2 = pads([4,5,6,7], dur=1)

    p1 >> proxy_1 # Assign the first to p1
    p1 >> proxy_2 # This replaces the instructions being followed by p1

#### Methods

##### `Attributes(cls)`

To be replaced by `Player.get_attributes()` 

##### `__add__(self, data)`

Change the degree modifier stream 

##### `__call__(self, **kwargs)`

Sends the next osc message event to SuperCollider and schedules this
Player in the clock based on the current clock time and this player's
current duration value. 

##### `__eq__(self, other)`

Return self==value.

##### `__getattribute__(self, name)`

Return getattr(self, name).

##### `__init__(self, name=None)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__invert__(self)`

Using the ~ syntax resets the player 

##### `__ne__(self, other)`

Return self!=value.

##### `__repr__(self)`

Return repr(self).

##### `__rshift__(self, other)`

Handles the allocation of SynthDef objects using >> syntax, other must be
an instance of `SynthDefProxy`, which is usually created when calling a
`SynthDef`

##### `__setattr__(self, name, value)`

Implement setattr(self, name, value).

##### `__sub__(self, data)`

Change the degree modifier stream 

##### `accompany(self, other, values=[0, 2, 4], debug=False)`

Similar to "follow" but when the value has changed 

##### `addfx(self, **kwargs)`

Not implemented - add an effect to the SynthDef bus on SuperCollider
after it has been triggered. 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in 'n' beats time
```
# Stop the player looping after 16 beats
p1 >> pads().after(16, "stop")
```

##### `attrmap(self, key1, key2, mapping)`

Sets the attribute for self.key2 to self.key1
altered with a mapping dictionary.

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

##### `every(self, occurence, cmd, *args, **kwargs)`

Every n beats, call a method (defined as a string) on the
object and use the args and kwargs. To call the method
every n-th beat of a timeframe, use the `cycle` keyword argument
to specify that timeframe.

::
    # Call the shuffle method every 4 beats

    p1.every(4, 'shuffle')

    # Call the stutter method on the 5th beat of every 8 beat cycle

    p1.every(5, 'stutter', 4, cycle=8)

    # If the method is not valid but *is* a valid Pattern method, that is called and reverted

    p1.every(4, 'palindrome')

##### `follow(self, other=False)`

Takes a Player object and then follows the notes 

##### `get_attr_and_method_name(self, cmd)`

Returns the attribute and method name from a string in the form
`"attr.method"` would return `"attr"` and `"method"`. If attr is not
present, it returns `"degree"` in place. 

##### `get_attributes(cls)`

Returns a list of possible keyword arguments for FoxDot players and effects 

##### `get_event(self)`

Returns a dictionary of attr -> now values 

##### `get_method_by_name(self, cmd)`

Returns the attribute name and method based on `cmd` which is a string.
Should be in form `"attr.method"`.

##### `get_prime_funcs(self, event)`

Finds and PGroupPrimes in event and returns the modulated event dictionary 

##### `get_synth_name(self, buf=0)`

Returns the real SynthDef name of the player. Useful only for "play" 
as there is a play1 and play2 SynthDef for playing audio files with
one or two channels respectively. 

##### `is_pattern_method(self, method_name, attr=degree)`

Returns True if the method is a valid method of `Pattern` 

##### `is_player_method(self, method_name, attr=degree)`

Returns True if the method is a valid method  of `Player` 

##### `kill(self)`

Removes this object from the Clock and resets itself

##### `largest_attribute(self, **kwargs)`

Returns the length of the largest nested tuple in the current event dict 

##### `lshift(self, n=1)`

Plays the event behind 

##### `map(self, other, mapping, otherattr=degree)`

p1 >> pads().map(b1, {0: {oct=[4,5], dur=PDur(3,8), 2: oct})     

##### `never(self, cmd, ident=None)`

Stops calling cmd on repeat 

##### `new_message(self, index=0, **kwargs)`

Returns the header of an osc message to be added to by osc_message() 

##### `now(self, attr=degree, x=0, **kwargs)`

Calculates the values for each attr to send to the server at the current clock time 

##### `num_key_references(self)`

Returns the number of 'references' for the
attr which references the most other players 

##### `number_attr(self, attr)`

Returns true if the attribute should be a number 

##### `number_of_layers(self, **kwargs)`

Returns the deepest nested item in the event 

##### `offbeat(self, dur=1)`

Off sets the next event occurence 

##### `only(self)`

Stops all players except this one 

##### `osc_message(self, index=0, **kwargs)`

Creates an OSC packet to play a SynthDef in SuperCollider,
use kwargs to force values in the packet, e.g. pan=1 will force ['pan', 1] 

##### `reset(self)`

Sets all Player attributes to 0 unless their default is specified by an effect. Also
can be called by using a tilde before the player variable. E.g. ~p1 

##### `reverse(self)`

Reverses every attribute stream 

##### `rhythm(self)`

Returns the players array of durations at this point in time 

##### `rotate(self, n=1)`

Rotates the values in the degree by 'n' 

##### `rshift(self, n=1)`

Plays the event in front 

##### `send(self, timestamp=None, **kwargs)`

Sends the current event data to SuperCollder.
Use kwargs to overide values in the current event 

##### `set_queue_block(self, queue_block)`

Gives this player object a reference to the other items that are 
scheduled at the same time 

##### `shuffle(self)`

Shuffles the degree of a player. 

##### `slider(self, start=0, on=1)`

Creates a glissando effect between notes 

##### `smap(self, kwargs)`

Like map but maps the degree to the sample attribute
        

##### `solo(self, action=1)`

Silences all players except this player. Undo the solo
by using `Player.solo(0)` 

##### `spread(self, on=0.125)`

Sets pan to (-1, 1) and pshift to (0, 0.125)

##### `stop(self, N=0)`

Removes the player from the Tempo clock and changes its internal
playing state to False in N bars time
- When N is 0 it stops immediately

##### `stop_calling_all(self)`

Stops all repeated methods. 

##### `strum(self, dur=0.025)`

Adds a delay to a Synth Envelope 

##### `stutter(self, amount=None, **kwargs)`

Plays the current note n-1 times. You can specify keywords. 

##### `test_for_circular_reference(self, attr, value, last_parent=None, last_key=None)`

Used to raise an exception if a player's attribute refers to itself e.g. `p1 >> pads(dur=p1.dur)` 

##### `unduplicate_durs(self, event)`

Converts values stored in event["dur"] in a tuple/PGroup into delays 

##### `unpack(self, item, debug=False)`

Converts a pgroup to floating point values and updates and time var or playerkey relations 

##### `update(self, synthdef, degree, **kwargs)`

Updates the attributes of the player. Called using the >> syntax.
        

##### `update_all_player_keys(self, ignore=[], event=None, **kwargs)`

Updates the internal values of player keys that have been accessed e.g. p1.pitch. If there is a delay,
then schedule a function to update the values in the future. 

##### `update_pattern_methods(self, attr)`

Update the 'current' version of a pattern based on its root and methods stored 

##### `update_pattern_root(self, attr)`

Update the base attribute pattern that methods are applied to 

##### `update_player_key(self, key, value, time)`

Forces object's dict uses PlayerKey instances
        

##### `versus_old(self, other, key=<lambda>, f=<built-in function max>)`

Takes another Player object and a function that takes
two player arguments and returns one, default is the higher
pitched

---

### `Group(self, *args)`



#### Methods

##### `__getattr__(self, name)`

Returns a Pattern object containing the desired attribute for each player in the group  

##### `__init__(self, *args)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__setattr__(self, name, value)`

Implement setattr(self, name, value).

##### `__str__(self)`

Return str(self).

---

### `GroupAttr(self, *args, **kwargs)`

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

#### Methods

##### `__call__(self, *args, **kwargs)`

Call self as a function.

---

### `rest(self, dur=1)`

Represents a rest when used with a Player's `dur` keyword
    

#### Methods

##### `__eq__(self, other)`

Return self==value.

##### `__ge__(self, other)`

Return self>=value.

##### `__gt__(self, other)`

Return self>value.

##### `__init__(self, dur=1)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__le__(self, other)`

Return self<=value.

##### `__lt__(self, other)`

Return self<value.

##### `__ne__(self, other)`

Return self!=value.

##### `__repr__(self)`

Return repr(self).

---

### `PlayerKeyException(self, *args, **kwargs)`

Common base class for all non-exit exceptions.

#### Methods

---

## Functions

## Data

