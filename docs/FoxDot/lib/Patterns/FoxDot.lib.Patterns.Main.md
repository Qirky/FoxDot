# `FoxDot.lib.Patterns.Main`

None

## Classes

### `EmptyItem(self)`

Can be used in a pattern and and is essentially not there 

#### Methods

---

### `GeneratorPattern(self)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

##### `getitem(self, index=None)`

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

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `convert_data(self, dtype=<type 'float'>)`

Makes a true copy and converts the data to a given data type 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(('self',), ('n',))`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `merge(self, value)`

Merge values into one PGroup 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `normalise(self)`

Returns the pattern with all values between 0 and 1 

##### `palindrome(('self',), ('a', 0)=0, ('b', None)=None)`

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

##### `pivot(('self',), ('i',))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(('self',), ('n',))`

Returns an n-length pattern from a sample

##### `scale_dur(self, n)`

Scales the dur values for all the items in self.data by n 

##### `shufflets(self, n)`

Returns a Pattern of 'n' number of PGroups made from shuffled
versions of the original Pattern 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `splice(self, seq, *seqs)`

Takes at least list / Pattern and creates a new Pattern by
adding a value from each pattern in turn to the new pattern.
e.g.
```
>>> P[0,1,2,3].splice([4,5,6,7],[8,9])
P[0,4,8,1,5,9,2,6,8,3,7,9]
```

##### `stretch(('self',), ('size',))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `Pattern(self, data=[])`

Base type pattern 

#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `convert_data(self, dtype=<type 'float'>)`

Makes a true copy and converts the data to a given data type 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(self, n)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `normalise(self)`

Returns the pattern with all values between 0 and 1 

##### `palindrome(self, a=0, b=None)`

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

##### `pivot(self, i)`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(self, n)`

Returns an n-length pattern from a sample

##### `shufflets(self, n)`

Returns a Pattern of 'n' number of PGroups made from shuffled
versions of the original Pattern 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `splice(self, seq, *seqs)`

Takes at least list / Pattern and creates a new Pattern by
adding a value from each pattern in turn to the new pattern.
e.g.
```
>>> P[0,1,2,3].splice([4,5,6,7],[8,9])
P[0,4,8,1,5,9,2,6,8,3,7,9]
```

##### `stretch(self, size)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PatternContainer(self, data=[])`



#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `convert_data(self, dtype=<type 'float'>)`

Makes a true copy and converts the data to a given data type 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop((('self',),), (('n',),))`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `normalise(self)`

Returns the pattern with all values between 0 and 1 

##### `palindrome((('self',),), (('a', 0), 0)=0, (('b', None), None)=None)`

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

##### `pivot((('self',),), (('i',),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample((('self',),), (('n',),))`

Returns an n-length pattern from a sample

##### `shufflets(self, n)`

Returns a Pattern of 'n' number of PGroups made from shuffled
versions of the original Pattern 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `splice(self, seq, *seqs)`

Takes at least list / Pattern and creates a new Pattern by
adding a value from each pattern in turn to the new pattern.
e.g.
```
>>> P[0,1,2,3].splice([4,5,6,7],[8,9])
P[0,4,8,1,5,9,2,6,8,3,7,9]
```

##### `stretch((('self',),), (('size',),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `metaPattern(self, data=[])`

Abstract base class for Patterns 

#### Methods

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `convert_data(self, dtype=<type 'float'>)`

Makes a true copy and converts the data to a given data type 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(((('self',),),), ((('n',),),))`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `normalise(self)`

Returns the pattern with all values between 0 and 1 

##### `palindrome(((('self',),),), ((('a', 0), 0), 0)=0, ((('b', None), None), None)=None)`

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

##### `pivot(((('self',),),), ((('i',),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(((('self',),),), ((('n',),),))`

Returns an n-length pattern from a sample

##### `shufflets(self, n)`

Returns a Pattern of 'n' number of PGroups made from shuffled
versions of the original Pattern 

##### `sort(self)`

Used in place of sorted(pattern) to force type 

##### `splice(self, seq, *seqs)`

Takes at least list / Pattern and creates a new Pattern by
adding a value from each pattern in turn to the new pattern.
e.g.
```
>>> P[0,1,2,3].splice([4,5,6,7],[8,9])
P[0,4,8,1,5,9,2,6,8,3,7,9]
```

##### `stretch(((('self',),),), ((('size',),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

## Functions

### `ClassPatternMethod(f)`

Decorator that makes a function into a metaPattern class method

### `Convert(*args)`

Returns tuples/PGroups as PGroups, and anything else as Patterns 

### `Format(data)`

None

### `PatternMethod(f)`

Decorator that makes a function into a metaPattern method

### `StaticPatternMethod(f)`

Decorator that makes a function into a metaPattern static  method

### `asStream(data)`

Forces any data into a [pattern] form 

### `group_modi(pgroup, index)`

Returns value from pgroup that modular indexes nested groups 

### `loop_pattern_func(f)`

Decorator for allowing any Pattern function to create
multiple Patterns by using Patterns or TimeVars as arguments 

### `loop_pattern_method(f)`

Decorator for allowing any Pattern method to create
multiple (or rather, longer) Patterns by using Patterns as arguments 

### `pattern_depth(pat)`

Returns the level of nested arrays 

### `patternclass(a, b)`

None

## Data

