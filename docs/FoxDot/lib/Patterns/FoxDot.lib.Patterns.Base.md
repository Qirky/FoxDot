# `FoxDot.lib.Patterns.Base`

None

## Classes

### `GeneratorPattern(self)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

##### `getitem(self, index)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PGroup(self, data=[], *args)`

Class to represent any groupings of notes as denoted by brackets.
PGroups should only be found within a Pattern object.

#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `make(self)`

This method automatically laces and groups the data 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `string(self)`

Returns a string made up of all the values:

PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" 

##### `loop(self, n)`

Repeats this pattern n times 

##### `choose(self)`

Returns one randomly selected item 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `scale_dur(self, n)`

Scales the dur values for all the items in self.data by n 

---

### `Pattern(self, data=[])`



#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `make(self)`

This method automatically laces and groups the data 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `string(self)`

Returns a string made up of all the values:

PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" 

##### `loop(self, n)`

Repeats this pattern n times 

##### `choose(self)`

Returns one randomly selected item 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `coeff(self)`

Returns a duration value relative to the type of pattern. Most patterns return val unchanged 

##### `getitem(self, key)`

Is called by __getitem__ 

---

### `PatternContainer(self, data=[])`



#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `make(self)`

This method automatically laces and groups the data 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `string(self)`

Returns a string made up of all the values:

PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" 

##### `loop(self, n)`

Repeats this pattern n times 

##### `choose(self)`

Returns one randomly selected item 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `coeff(self)`

Returns a duration value relative to the type of pattern. Most patterns return val unchanged 

---

### `Pgroup(self, data=[], *args)`

Class to represent any groupings of notes as denoted by brackets.
PGroups should only be found within a Pattern object.

#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `make(self)`

This method automatically laces and groups the data 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `string(self)`

Returns a string made up of all the values:

PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" 

##### `loop(self, n)`

Repeats this pattern n times 

##### `choose(self)`

Returns one randomly selected item 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `scale_dur(self, n)`

Scales the dur values for all the items in self.data by n 

---

### `Shared_Time_PGroup(self, data=[], *args)`



#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `make(self)`

This method automatically laces and groups the data 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `string(self)`

Returns a string made up of all the values:

PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" 

##### `loop(self, n)`

Repeats this pattern n times 

##### `choose(self)`

Returns one randomly selected item 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `scale_dur(self, n)`

Scales the dur values for all the items in self.data by n 

---

### `dots(self)`

Class for representing long Patterns in strings 

#### Methods

---

### `metaPattern(self, data=[])`

Abstract base class for Patterns 

#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `make(self)`

This method automatically laces and groups the data 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `string(self)`

Returns a string made up of all the values:

PSeq([1,"x",(1,1),("x","x")]).string() -> "1x11xx" 

##### `loop(self, n)`

Repeats this pattern n times 

##### `choose(self)`

Returns one randomly selected item 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `coeff(self)`

Returns a duration value relative to the type of pattern. Most patterns return val unchanged 

##### `getitem(self, key)`

Is called by __getitem__ 

---

## Functions

### `Convert(*args)`

Returns tuples/PGroups as PGroups, and anything else as Patterns 

### `Dominant(*patterns)`

None

### `Format(data)`

None

### `asStream(data)`

Forces any data into a [pattern] form 

## Data

