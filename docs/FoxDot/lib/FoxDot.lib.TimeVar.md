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

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

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

Zips a pattern with a modified version of itself 

##### `length(self)`

Returns the duration of one full cycle in beats 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `new(self, other)`

Returns a new TimeVar object 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `shufflets(self, n)`

Returns a Pattern of 'n' number of PGroups made from shuffled
versions of the original Pattern 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a string made up of all the values:

PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" 

##### `update(self, values, dur=None, **kwargs)`

Updates the TimeVar with new values 

---

### `_continuous_var(self, *args, **kwargs)`



#### Methods

##### `__rshift__(self, other)`

var >> var([0,1,2,3],[4,8])
var >> ([0,1,2,3],[4,8])

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

