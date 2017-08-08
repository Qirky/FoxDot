# `FoxDot.lib.Patterns.PGroups`

None

## Classes

### `PGroupAnd(self, args)`

Unused 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(((((((((('self',),),),),),),),),), ((((((((('n',),),),),),),),),))`

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

##### `palindrome(((((((((('self',),),),),),),),),), ((((((((('a', 0), 0), 0), 0), 0), 0), 0), 0), 0)=0, ((((((((('b', None), None), None), None), None), None), None), None), None)=None)`

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

##### `pivot(((((((((('self',),),),),),),),),), ((((((((('i',),),),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(((((((((('self',),),),),),),),),), ((((((((('n',),),),),),),),),))`

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

##### `stretch(((((((((('self',),),),),),),),),), ((((((((('size',),),),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupDiv(self, *args, **kwargs)`

Stutter every other request 

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

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(((((('self',),),),),), ((((('n',),),),),))`

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

##### `palindrome(((((('self',),),),),), ((((('a', 0), 0), 0), 0), 0)=0, ((((('b', None), None), None), None), None)=None)`

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

##### `pivot(((((('self',),),),),), ((((('i',),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(((((('self',),),),),), ((((('n',),),),),))`

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

##### `stretch(((((('self',),),),),), ((((('size',),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupFloorDiv(self, data=[], *args)`

Unused 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(((((((('self',),),),),),),), ((((((('n',),),),),),),))`

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

##### `palindrome(((((((('self',),),),),),),), ((((((('a', 0), 0), 0), 0), 0), 0), 0)=0, ((((((('b', None), None), None), None), None), None), None)=None)`

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

##### `pivot(((((((('self',),),),),),),), ((((((('i',),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(((((((('self',),),),),),),), ((((((('n',),),),),),),))`

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

##### `stretch(((((((('self',),),),),),),), ((((((('size',),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupMod(self, data=[], *args)`

Unused 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop((((('self',),),),), (((('n',),),),))`

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

##### `palindrome((((('self',),),),), (((('a', 0), 0), 0), 0)=0, (((('b', None), None), None), None)=None)`

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

##### `pivot((((('self',),),),), (((('i',),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample((((('self',),),),), (((('n',),),),))`

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

##### `stretch((((('self',),),),), (((('size',),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupOr(self, data=[], *args)`

Unused 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(((((((((((('self',),),),),),),),),),),), ((((((((((('n',),),),),),),),),),),))`

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

##### `palindrome(((((((((((('self',),),),),),),),),),),), ((((((((((('a', 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0)=0, ((((((((((('b', None), None), None), None), None), None), None), None), None), None), None)=None)`

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

##### `pivot(((((((((((('self',),),),),),),),),),),), ((((((((((('i',),),),),),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(((((((((((('self',),),),),),),),),),),), ((((((((((('n',),),),),),),),),),),))`

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

##### `stretch(((((((((((('self',),),),),),),),),),),), ((((((((((('size',),),),),),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupPlus(self, data=[], *args)`

Stutters the values over the length of and event's 'sus' 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop((((((((((((('self',),),),),),),),),),),),), (((((((((((('n',),),),),),),),),),),),))`

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

##### `palindrome((((((((((((('self',),),),),),),),),),),),), (((((((((((('a', 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0)=0, (((((((((((('b', None), None), None), None), None), None), None), None), None), None), None), None)=None)`

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

##### `pivot((((((((((((('self',),),),),),),),),),),),), (((((((((((('i',),),),),),),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample((((((((((((('self',),),),),),),),),),),),), (((((((((((('n',),),),),),),),),),),),))`

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

##### `stretch((((((((((((('self',),),),),),),),),),),),), (((((((((((('size',),),),),),),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupPow(self, data=[], *args)`

Stutters a shuffled version the values over the length of and event's 'dur' 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop(((((((((((((('self',),),),),),),),),),),),),), ((((((((((((('n',),),),),),),),),),),),),))`

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

##### `palindrome(((((((((((((('self',),),),),),),),),),),),),), ((((((((((((('a', 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0)=0, ((((((((((((('b', None), None), None), None), None), None), None), None), None), None), None), None), None)=None)`

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

##### `pivot(((((((((((((('self',),),),),),),),),),),),),), ((((((((((((('i',),),),),),),),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample(((((((((((((('self',),),),),),),),),),),),),), ((((((((((((('n',),),),),),),),),),),),),))`

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

##### `stretch(((((((((((((('self',),),),),),),),),),),),),), ((((((((((((('size',),),),),),),),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupPrime(self, data=[], *args)`



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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop((((((('self',),),),),),), (((((('n',),),),),),))`

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

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample((((((('self',),),),),),), (((((('n',),),),),),))`

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

##### `stretch((((((('self',),),),),),), (((((('size',),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupStar(self, data=[], *args)`

Stutters the values over the length of and event's 'dur' 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop((((((((((((((('self',),),),),),),),),),),),),),), (((((((((((((('n',),),),),),),),),),),),),),))`

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

##### `palindrome((((((((((((((('self',),),),),),),),),),),),),),), (((((((((((((('a', 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0), 0)=0, (((((((((((((('b', None), None), None), None), None), None), None), None), None), None), None), None), None), None)=None)`

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

##### `pivot((((((((((((((('self',),),),),),),),),),),),),),), (((((((((((((('i',),),),),),),),),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample((((((((((((((('self',),),),),),),),),),),),),),), (((((((((((((('n',),),),),),),),),),),),),),))`

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

##### `stretch((((((((((((((('self',),),),),),),),),),),),),),), (((((((((((((('size',),),),),),),),),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Used for SamplePlayerStrings 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupSub(self, data=[], *args)`

Unused 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop((((((((((('self',),),),),),),),),),), (((((((((('n',),),),),),),),),),))`

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

##### `palindrome((((((((((('self',),),),),),),),),),), (((((((((('a', 0), 0), 0), 0), 0), 0), 0), 0), 0), 0)=0, (((((((((('b', None), None), None), None), None), None), None), None), None), None)=None)`

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

##### `pivot((((((((((('self',),),),),),),),),),), (((((((((('i',),),),),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample((((((((((('self',),),),),),),),),),), (((((((((('n',),),),),),),),),),))`

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

##### `stretch((((((((((('self',),),),),),),),),),), (((((((((('size',),),),),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

### `PGroupXor(self, data=[], *args)`

Unused 

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

##### `change_state(self)`

To be overridden by any PGroupPrime that changes state after access by a Player 

##### `choose(self)`

Returns one randomly selected item 

##### `contains_nest(self)`

Returns true if the pattern contains a nest 

##### `force_values(self)`

Recursively (in place) forces changeable values into non-changeable 

##### `getitem(self, key)`

Is called by __getitem__ 

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `loop((((((((('self',),),),),),),),), (((((((('n',),),),),),),),))`

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

##### `palindrome((((((((('self',),),),),),),),), (((((((('a', 0), 0), 0), 0), 0), 0), 0), 0)=0, (((((((('b', None), None), None), None), None), None), None), None)=None)`

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

##### `pivot((((((((('self',),),),),),),),), (((((((('i',),),),),),),),))`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `sample((((((((('self',),),),),),),),), (((((((('n',),),),),),),),))`

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

##### `stretch((((((((('self',),),),),),),),), (((((((('size',),),),),),),),))`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `unduplicate(self)`

Removes any consecutive duplicate numbers from a Pattern 

---

## Functions

## Data

