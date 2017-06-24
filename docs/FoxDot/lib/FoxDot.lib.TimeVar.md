# `FoxDot.lib.TimeVar`

Time-Dependent Variable Base Class
==================================

- Function of time
- Duck typing

- Explain inf stages: 0, 1, 2, 3

    - Stage 0: No inf value present
    - Stage 1: inf value is present but other values haven't been accessed yet
    - Stage 2: Starting values have been accessed so we are free to return a value for inf duration
    - State 3: Returning the inf value

## Classes

### `Pvar(self, values, dur=None, **kwargs)`

Pvar([pat1, pat2], durs) 

#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__rshift__(self, other)`

var >> var([0,1,2,3],[4,8])
var >> ([0,1,2,3],[4,8])

##### `_bpm_cycle_dur(self)`

Returns the time, in seconds, for a var to loop to its original
value and duration if this var is a bpm value. 

##### `_bpm_to_beats(self, duration, start=0)`

If self.data are series of bpm, how many beats occur in
the time frame 'duration'. Used in TempoClock 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, i=2)`

Merges and laces the first and last two items such that a drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `calculate(self, val)`

Returns val as modified by its dependencies 

##### `choose(self)`

Returns one randomly selected item 

##### `coeff(self)`

Returns a duration value relative to the type of pattern. Most patterns return val unchanged 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `current_time(self, beat=None)`

Returns the current beat value 

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

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `length(self)`

Returns the duration of one full cycle in beats 

##### `loop((((((('self',),),),),),), (((((('n',),),),),),))`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `new(self, other)`

Returns a new TimeVar object 

##### `normalise(self)`

Returns the pattern with all values between 0 and 1 

##### `palindrome((((((('self',),),),),),), (((((('a', 0), 0), 0), 0), 0), 0)=0, (((((('b', None), None), None), None), None), None)=None)`

Returns the original pattern with mirrored version of itself appended.
a removes values from the middle of the pattern, if positive.
b removes values from the end of the pattern, should be negative.

e.g.

>>> P[:4].palindrome()
P[0, 1, 2, 3, 3, 2, 1, 0]
>>> P[:4].palindrome(1)
P[0, 1, 2, 3, 2, 1, 0]
>>> P[:4].palindrome(-1)
P[0, 1, 2, 3, 3, 2, 1]
>>> P[:4].palindrome(1,-1)
P[0, 1, 2, 3, 2, 1]

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `pivot((((((('self',),),),),),), (((((('i',),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `shufflets(self, n)`

Returns a Pattern of 'n' number of PGroups made from shuffled
versions of the original Pattern 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `stretch((((((('self',),),),),),), (((((('size',),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

##### `update(self, values, dur=None, **kwargs)`

Updates the TimeVar with new values 

---

### `_continuous_var(self, *args, **kwargs)`



#### Methods

##### `__rshift__(self, other)`

var >> var([0,1,2,3],[4,8])
var >> ([0,1,2,3],[4,8])

##### `_bpm_cycle_dur(self)`

Returns the time, in seconds, for a var to loop to its original
value and duration if this var is a bpm value. 

##### `_bpm_to_beats(self, duration, start=0)`

If self.data are series of bpm, how many beats occur in
the time frame 'duration'. Used in TempoClock 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `calculate(self, val)`

Returns val as modified by its dependencies 

##### `current_time(self, beat=None)`

Returns the current beat value 

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

##### `length(self)`

Returns the duration of one full cycle in beats 

##### `new(self, other)`

Returns a new TimeVar object 

##### `update(self, values, dur=None, **kwargs)`

Updates the TimeVar with new values 

---

### `_inf(self)`

Used in TimeVars to stay on certain values until re-evaluated 

#### Methods

---

### `expvar(self, *args, **kwargs)`



#### Methods

##### `__rshift__(self, other)`

var >> var([0,1,2,3],[4,8])
var >> ([0,1,2,3],[4,8])

##### `_bpm_cycle_dur(self)`

Returns the time, in seconds, for a var to loop to its original
value and duration if this var is a bpm value. 

##### `_bpm_to_beats(self, duration, start=0)`

If self.data are series of bpm, how many beats occur in
the time frame 'duration'. Used in TempoClock 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `calculate(self, val)`

Returns val as modified by its dependencies 

##### `current_time(self, beat=None)`

Returns the current beat value 

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

##### `length(self)`

Returns the duration of one full cycle in beats 

##### `new(self, other)`

Returns a new TimeVar object 

##### `update(self, values, dur=None, **kwargs)`

Updates the TimeVar with new values 

---

### `linvar(self, *args, **kwargs)`



#### Methods

##### `__rshift__(self, other)`

var >> var([0,1,2,3],[4,8])
var >> ([0,1,2,3],[4,8])

##### `_bpm_cycle_dur(self)`

Returns the time, in seconds, for a var to loop to its original
value and duration if this var is a bpm value. 

##### `_bpm_to_beats(self, duration, start=0)`

If self.data are series of bpm, how many beats occur in
the time frame 'duration'. Used in TempoClock 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `calculate(self, val)`

Returns val as modified by its dependencies 

##### `current_time(self, beat=None)`

Returns the current beat value 

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

##### `length(self)`

Returns the duration of one full cycle in beats 

##### `new(self, other)`

Returns a new TimeVar object 

##### `update(self, values, dur=None, **kwargs)`

Updates the TimeVar with new values 

---

### `var(self, values, dur=None, **kwargs)`

Var(values [,durs=[4]]) 

#### Methods

##### `__rshift__(self, other)`

var >> var([0,1,2,3],[4,8])
var >> ([0,1,2,3],[4,8])

##### `_bpm_cycle_dur(self)`

Returns the time, in seconds, for a var to loop to its original
value and duration if this var is a bpm value. 

##### `_bpm_to_beats(self, duration, start=0)`

If self.data are series of bpm, how many beats occur in
the time frame 'duration'. Used in TempoClock 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `calculate(self, val)`

Returns val as modified by its dependencies 

##### `current_time(self, beat=None)`

Returns the current beat value 

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

##### `length(self)`

Returns the duration of one full cycle in beats 

##### `new(self, other)`

Returns a new TimeVar object 

##### `update(self, values, dur=None, **kwargs)`

Updates the TimeVar with new values 

---

## Functions

### `_timevar_index(self, key)`

None

### `fetch(func)`

Function to wrap basic lambda operators for TimeVars  

## Data

#### `inf = 2147483647`

