# `FoxDot.lib.Scale`

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

## Functions

### `choose()`

Scale.choose() -> Returns a random scale object 

### `names()`

Returns a list of all the scales by name 

## Data

#### `chromatic = P[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]`

#### `default = P[0, 2, 4, 5, 7, 9, 11]`

#### `dorian = P[0, 2, 3, 5, 7, 9, 10]`

#### `egyptian = P[0, 2, 5, 7, 10]`

#### `fibonacci = P[0.0, 1.5, 3.3333333333333335, 4.800000000000001, 6.5, 8.076923076923077, 9.714285714285715]`

#### `freq = P[inf]`

#### `harmonicMajor = P[0, 2, 4, 5, 7, 8, 11]`

#### `harmonicMinor = P[0, 2, 3, 5, 7, 8, 11]`

#### `indian = P[0, 4, 5, 7, 10]`

#### `locrian = P[0, 1, 3, 5, 6, 8, 10]`

#### `locrianMajor = P[0, 2, 4, 5, 6, 8, 10]`

#### `lydian = P[0, 2, 4, 6, 7, 9, 11]`

#### `lydianMinor = P[0, 2, 4, 6, 7, 8, 10]`

#### `major = P[0, 2, 4, 5, 7, 9, 11]`

#### `majorPentatonic = P[0, 2, 4, 7, 9]`

#### `melodicMajor = P[0, 2, 4, 5, 7, 8, 11]`

#### `melodicMinor = P[0, 2, 3, 5, 7, 9, 11]`

#### `minor = P[0, 2, 3, 5, 7, 8, 10]`

#### `minorPentatonic = P[0, 3, 5, 7, 10]`

#### `mixolydian = P[0, 2, 4, 5, 7, 9, 10]`

#### `phyrgian = P[0, 1, 3, 5, 7, 8, 10]`

#### `prometheus = P[0, 2, 4, 6, 11]`

#### `zgi = P[0, 2, 5, 7, 9]`

