# FoxDot.lib.Scale

None

## Classes

### `PentatonicScale(self, scale)`



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

### `Scale(self, name, *args)`



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

### `_freq(self)`



#### Methods

---

## Functions

### `choose()`

Scale.choose() -> Returns a random scale object 

### `names()`

Returns a list of all the scales by name 

## Data

### `chromatic`



### `default`



### `dorian`



### `egyptian`



### `fibonacci`



### `freq`



### `harmonicMajor`



### `harmonicMinor`



### `indian`



### `locrian`



### `locrianMajor`



### `lydian`



### `lydianMinor`



### `major`



### `majorPentatonic`



### `melodicMajor`



### `melodicMinor`



### `minor`



### `minorPentatonic`



### `mixolydian`



### `phyrgian`



### `prometheus`



### `zgi`



