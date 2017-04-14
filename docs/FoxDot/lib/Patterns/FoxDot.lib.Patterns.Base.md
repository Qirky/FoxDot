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

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `merge(self, value)`

Merge values into one PGroup 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `scale_dur(self, n)`

Scales the dur values for all the items in self.data by n 

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

---

### `Pattern(self, data=[])`



#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `choose(self)`

Returns one randomly selected item 

##### `coeff(self)`

Returns a duration value relative to the type of pattern. Most patterns return val unchanged 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

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

---

### `PatternContainer(self, data=[])`



#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `choose(self)`

Returns one randomly selected item 

##### `coeff(self)`

Returns a duration value relative to the type of pattern. Most patterns return val unchanged 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

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

---

### `Pgroup(self, data=[], *args)`

Class to represent any groupings of notes as denoted by brackets.
PGroups should only be found within a Pattern object.

#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `merge(self, value)`

Merge values into one PGroup 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `scale_dur(self, n)`

Scales the dur values for all the items in self.data by n 

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

---

### `Shared_Time_PGroup(self, data=[], *args)`



#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `merge(self, value)`

Merge values into one PGroup 

##### `pipe(self, pattern)`

Concatonates this patterns stream with another 

##### `scale_dur(self, n)`

Scales the dur values for all the items in self.data by n 

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

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `choose(self)`

Returns one randomly selected item 

##### `coeff(self)`

Returns a duration value relative to the type of pattern. Most patterns return val unchanged 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `flat(self)`

P.flat() -> un-nested pattern 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

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

