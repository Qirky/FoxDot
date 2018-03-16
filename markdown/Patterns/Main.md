# `Main`

Contains classes `Pattern` and `PGroup` and the base class for `GeneratorPattern` (see Generators.py).

## Classes

### `EmptyItem(self)`

Can be used in a pattern and and is essentially not there 

#### Methods

##### `__init__(self)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

---

### `GeneratorPattern(self, **kwargs)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

##### `__init__(self, **kwargs)`

Initialize an instance.

Optional argument x controls seeding, as for Random.seed().

##### `__new__(cls, *args, **kwargs)`

Override random.Random using first argument as a seed 

##### `__reduce__(self)`

helper for pickle

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, int=<class 'int'>, maxsize=9007199254740992, type=<class 'type'>, Method=<class 'method'>, BuiltinMethod=<class 'builtin_function_or_method'>)`

Return a random int in the range [0,n).  Raises ValueError if n==0.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

##### `choices(self, population, weights=None)`

Return a k sized list of population elements chosen with replacement.

If the relative weights or cumulative weights are not specified,
the selections are made with equal probability.

##### `dup(self, n=2)`

Returns a PGroup with n lots of the Generator 

##### `expovariate(self, lambd)`

Exponential distribution.

lambd is 1.0 divided by the desired mean.  It should be
nonzero.  (The parameter would be called "lambda", but that is
a reserved word in Python.)  Returned values range from 0 to
positive infinity if lambd is positive, and from negative
infinity to 0 if lambd is negative.

##### `gammavariate(self, alpha, beta)`

Gamma distribution.  Not the gamma function!

Conditions on the parameters are alpha > 0 and beta > 0.

The probability distribution function is:

            x ** (alpha - 1) * math.exp(-x / beta)
  pdf(x) =  --------------------------------------
              math.gamma(alpha) * beta ** alpha

##### `gauss(self, mu, sigma)`

Gaussian distribution.

mu is the mean, and sigma is the standard deviation.  This is
slightly faster than the normalvariate() function.

Not thread-safe without a lock around calls.

##### `getitem(self, index=None, *args)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

##### `map(self, mapping, default=0)`

Using .transform() to map values via a dictionary

::
    a = PRand([0,1])
    b = a.map({0: 16, 1: 25})

##### `new(self, other, func=Nil)`

Creates a new `GeneratorPattern` that references
this pattern but returns a modified value based on
func. 

##### `normalvariate(self, mu, sigma)`

Normal distribution.

mu is the mean, and sigma is the standard deviation.

##### `paretovariate(self, alpha)`

Pareto distribution.  alpha is the shape parameter.

##### `randint(self, a, b)`

Return random integer in range [a, b], including both end points.
        

##### `randrange(self, start, stop=None, step=1, _int=<class 'int'>)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence or set.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use range as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(range(10000000), 60)

##### `seed(self, a=None, version=2)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If *a* is an int, all bits are used.

For version 2 (the default), all of the bits are used if *a* is a str,
bytes, or bytearray.  For version 1 (provided for reproducing random
sequences from older versions of Python), the algorithm for str and
bytes generates a narrower range of seeds.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

Shuffle list x in place, and return None.

Optional argument random is a 0-argument function returning a
random float in [0.0, 1.0); if it is the default None, the
standard random.random will be used.

##### `transform(self, func)`

Use func, which should take 1 argument, to transform the values in a generator pattern. Trivial example:
myGenerator.transform(lambda x: 0 if x in (0,1,2) else 3)

##### `triangular(self, low=0.0, high=1.0, mode=None)`

Triangular distribution.

Continuous distribution bounded by given lower and upper limits,
and having a given mode value in-between.

http://en.wikipedia.org/wiki/Triangular_distribution

##### `uniform(self, a, b)`

Get a random number in the range [a, b) or [a, b] depending on rounding.

##### `vonmisesvariate(self, mu, kappa)`

Circular data distribution.

mu is the mean angle, expressed in radians between 0 and 2*pi, and
kappa is the concentration parameter, which must be greater than or
equal to zero.  If kappa is equal to zero, this distribution reduces
to a uniform random angle over the range 0 to 2*pi.

##### `weibullvariate(self, alpha, beta)`

Weibull distribution.

alpha is the scale parameter and beta is the shape parameter.

---

### `PGroup(self, seq=[], *args)`

Class to represent any groupings of notes as denoted by brackets.
PGroups should only be found within a Pattern object.

#### Methods

##### `__eq__(self, other)`

Return self==value.

##### `__ge__(self, other)`

Return self>=value.

##### `__getitem__(self, key)`

Overrides the Pattern.__getitem__ to allow indexing
by TimeVar and PlayerKey instances. 

##### `__gt__(self, other)`

Return self>value.

##### `__hash__(self)`

Return hash(self).

##### `__init__(self, seq=[], *args)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__invert__(self)`

Using the ~ symbol as a prefix to a Pattern will reverse it.
>>> a = P[:4]
>>> print(a, ~a)
P[0, 1, 2, 3], P[3, 2, 1, 0]

##### `__iter__(self)`

Returns a generator object for this Pattern 

##### `__key(self)`

Returns a tuple of information to identify this Pattern 

##### `__le__(self, other)`

Return self<=value.

##### `__len__(self)`

Returns the *expanded* length of the pattern such that if the pattern is laced, the
value is the length of the list multiplied by the lowest-common-multiple of the lengths
of nested patterns. e.g. the following are identical:
```
>>> print( len(P[0,1,2,[3,4]]) )
8
>>> print( len(P[0,1,2,3,0,1,2,4]) )
8
```

##### `__lt__(self, other)`

Return self<value.

##### `__ne__(self, other)`

Return self!=value.

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__repr__(self)`

Return repr(self).

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `__str__(self)`

Return str(self).

##### `accum(self, *args)`

Returns a Pattern that is equivalent to list of sums of that
Pattern up to that index.

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `arp(self, arp_pattern)`

Return a new Pattern with each item repeated len(arp_pattern) times
and incremented by arp_pattern. Useful for arpeggiating. e.g.
```
>>> P[0, 1, 2, 3].arp([0, 2])
P[0, 2, 1, 3, 2, 4, 3, 5]
```

##### `asGroup(self)`

Returns the Pattern as a PGroup 

##### `bubble(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `calculate_time(self, dur)`

Returns a PGroup of durations to use as the delay argument
when this is a sub-class of `PGroupPrime` 

##### `choose(self)`

Returns one randomly selected item 

##### `convert_data(self, dtype=<class 'float'>, *args, **kwargs)`

Makes a true copy and converts the data to a given data type 

##### `copy(self)`

Returns a copy of the Pattern such that alterations to the
Pattern.data do not affect the original.

##### `count(self, item)`

Returns the number of occurrences of item in the Pattern

##### `deep_shuffle(self, n=1)`

Returns a new Pattern with shuffled contents and shuffles
any nested patterns. To shuffle the contents of nested patterns
with the rest of the Pattern's contents, use `true_shuffle`.

##### `duplicate(self, *args)`

Repeats this pattern n times but keep nested pattern values 

##### `eq(self, other)`

equals operator 

##### `every(self, n, method, *args, **kwargs)`

Returns the pattern looped n-1 times then appended with
the version returned when method is called on it. 

##### `flatten(self)`

Returns a nested PGroup as un-nested e.g.
::

    >>> P(0,(3,5)).flatten()
    P(0, 3, 5)

##### `get_behaviour(self)`

Returns a function that modulates a player event dictionary 

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `getitem(self, key, get_generator=False)`

Called by __getitem__() 

##### `group(self)`

Returns the Pattern as a PGroup 

##### `has_behaviour(self)`

Returns True if this is a PGroupPrime or any elements are
instances of PGroupPrime or its sub-classes

##### `help(cls)`

Prints the Pattern class docstring to the console 

##### `invert(self)`

Inverts the values with the Pattern.
        

##### `items(self)`

Returns a generator object equivalent to using enumerate() 

##### `iter(self, *args)`

Repeats this pattern n times but doesn't take nested pattern into account for length

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `limit(self, *args)`

Returns a new Pattern generated by adding elements from
this Pattern to a new list and repeatedly calling
`func()` on this list until `func(l)` is greater than `value`
e.g.
```
>>> print( P[0, 1, 2, 3].limit(sum, 10) )
P[0, 1, 2, 3, 0, 1, 2]
```

##### `loop(self, *args)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `map(self, func)`

Returns a Pattern that calls `func` on each item 

##### `merge(self, value)`

Merge values into one PGroup 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `ne(self, other)`

Not equals operator 

##### `norm(self)`

Returns the pattern with all values between 0 and 1 

##### `offlayer(self, dur, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `palindrome(self, *args)`

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

##### `pivot(self, *args)`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `reverse(self)`

Reverses the contents of the Pattern. Nested patterns are
not reversed. To reverse the contents of nester patterns
use `Pattern.mirror()`

##### `sample(self, *args)`

Returns an n-length pattern from a sample

##### `shuffle(self, n=1)`

Returns a new Pattern with shuffled contents. Note: nested patterns
stay together. To shuffle the contents of nested patterns, use
`deep_shuffle` or `true_shuffle`.

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

##### `startswith(self, prefix)`

Returns True if the first item in the Pattern is equal to prefix 

##### `stretch(self, *args)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `stutter(self, n=2)`

Returns a new Pattern with each item repeated by `n`. Use
a list of numbers for stutter different items by different
amount. e.g.
```
>>> P[0, 1, 2, 3].stutter([1,3])
P[0, 1, 1, 1, 2, 3, 3, 3]
```

##### `true_copy(self, new_data=None)`

Returns a copy of the Pattern such that items within the
Pattern hold the same state as the original.

##### `true_shuffle(self, n=1)`

Returns a new Pattern with completely shuffle contents such
that nested Patterns are shuffled within the larger Pattern

##### `undup(self)`

Removes any consecutive duplicate numbers from a Pattern 

##### `zip(self, other, dtype=None)`

Zips two patterns together. If one item is a tuple, it extends the tuple / PGroup
i.e. arrow_zip([(0,1),3], [2]) -> [(0,1,2),(3,2)]

##### `zipx(self, other)`

Returns a `Pattern` of `PGroups`, where each `PGroup` contains the i-th
element from each of the argument sequences. The length of the pattern
is the lowest common multiple of the lengths of the two joining patterns. 

---

### `Pattern(self, data=[])`

Base type pattern 

#### Methods

##### `__eq__(self, other)`

Return self==value.

##### `__ge__(self, other)`

Return self>=value.

##### `__getitem__(self, key)`

Overrides the Pattern.__getitem__ to allow indexing
by TimeVar and PlayerKey instances. 

##### `__gt__(self, other)`

Return self>value.

##### `__init__(self, data=[])`

Initialize self.  See help(type(self)) for accurate signature.

##### `__invert__(self)`

Using the ~ symbol as a prefix to a Pattern will reverse it.
>>> a = P[:4]
>>> print(a, ~a)
P[0, 1, 2, 3], P[3, 2, 1, 0]

##### `__iter__(self)`

Returns a generator object for this Pattern 

##### `__le__(self, other)`

Return self<=value.

##### `__len__(self)`

Returns the *expanded* length of the pattern such that if the pattern is laced, the
value is the length of the list multiplied by the lowest-common-multiple of the lengths
of nested patterns. e.g. the following are identical:
```
>>> print( len(P[0,1,2,[3,4]]) )
8
>>> print( len(P[0,1,2,3,0,1,2,4]) )
8
```

##### `__lt__(self, other)`

Return self<value.

##### `__ne__(self, other)`

Return self!=value.

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__repr__(self)`

Return repr(self).

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `__str__(self)`

Return str(self).

##### `accum(self, *args)`

Returns a Pattern that is equivalent to list of sums of that
Pattern up to that index.

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `arp(self, arp_pattern)`

Return a new Pattern with each item repeated len(arp_pattern) times
and incremented by arp_pattern. Useful for arpeggiating. e.g.
```
>>> P[0, 1, 2, 3].arp([0, 2])
P[0, 2, 1, 3, 2, 4, 3, 5]
```

##### `asGroup(self)`

Returns the Pattern as a PGroup 

##### `bubble(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `choose(self)`

Returns one randomly selected item 

##### `convert_data(self, dtype=<class 'float'>, *args, **kwargs)`

Makes a true copy and converts the data to a given data type 

##### `copy(self)`

Returns a copy of the Pattern such that alterations to the
Pattern.data do not affect the original.

##### `count(self, item)`

Returns the number of occurrences of item in the Pattern

##### `deep_shuffle(self, n=1)`

Returns a new Pattern with shuffled contents and shuffles
any nested patterns. To shuffle the contents of nested patterns
with the rest of the Pattern's contents, use `true_shuffle`.

##### `duplicate(self, *args)`

Repeats this pattern n times but keep nested pattern values 

##### `every(self, n, method, *args, **kwargs)`

Returns the pattern looped n-1 times then appended with
the version returned when method is called on it. 

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `getitem(self, key, get_generator=False)`

Called by __getitem__() 

##### `group(self)`

Returns the Pattern as a PGroup 

##### `help(cls)`

Prints the Pattern class docstring to the console 

##### `invert(self)`

Inverts the values with the Pattern.
        

##### `items(self)`

Returns a generator object equivalent to using enumerate() 

##### `iter(self, *args)`

Repeats this pattern n times but doesn't take nested pattern into account for length

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `limit(self, *args)`

Returns a new Pattern generated by adding elements from
this Pattern to a new list and repeatedly calling
`func()` on this list until `func(l)` is greater than `value`
e.g.
```
>>> print( P[0, 1, 2, 3].limit(sum, 10) )
P[0, 1, 2, 3, 0, 1, 2]
```

##### `loop(self, *args)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `map(self, func)`

Returns a Pattern that calls `func` on each item 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `norm(self)`

Returns the pattern with all values between 0 and 1 

##### `offlayer(self, dur, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `palindrome(self, *args)`

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

##### `pivot(self, *args)`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `reverse(self)`

Reverses the contents of the Pattern. Nested patterns are
not reversed. To reverse the contents of nester patterns
use `Pattern.mirror()`

##### `sample(self, *args)`

Returns an n-length pattern from a sample

##### `shuffle(self, n=1)`

Returns a new Pattern with shuffled contents. Note: nested patterns
stay together. To shuffle the contents of nested patterns, use
`deep_shuffle` or `true_shuffle`.

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

##### `startswith(self, prefix)`

Returns True if the first item in the Pattern is equal to prefix 

##### `stretch(self, *args)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `stutter(self, n=2)`

Returns a new Pattern with each item repeated by `n`. Use
a list of numbers for stutter different items by different
amount. e.g.
```
>>> P[0, 1, 2, 3].stutter([1,3])
P[0, 1, 1, 1, 2, 3, 3, 3]
```

##### `true_copy(self, new_data=None)`

Returns a copy of the Pattern such that items within the
Pattern hold the same state as the original.

##### `true_shuffle(self, n=1)`

Returns a new Pattern with completely shuffle contents such
that nested Patterns are shuffled within the larger Pattern

##### `undup(self)`

Removes any consecutive duplicate numbers from a Pattern 

##### `zip(self, other, dtype=None)`

Zips two patterns together. If one item is a tuple, it extends the tuple / PGroup
i.e. arrow_zip([(0,1),3], [2]) -> [(0,1,2),(3,2)]

##### `zipx(self, other)`

Returns a `Pattern` of `PGroups`, where each `PGroup` contains the i-th
element from each of the argument sequences. The length of the pattern
is the lowest common multiple of the lengths of the two joining patterns. 

---

### `PatternContainer(self, data=[])`

Abstract base class for Patterns 

#### Methods

##### `__eq__(self, other)`

Return self==value.

##### `__ge__(self, other)`

Return self>=value.

##### `__getitem__(self, key)`

Overrides the Pattern.__getitem__ to allow indexing
by TimeVar and PlayerKey instances. 

##### `__gt__(self, other)`

Return self>value.

##### `__init__(self, data=[])`

Initialize self.  See help(type(self)) for accurate signature.

##### `__invert__(self)`

Using the ~ symbol as a prefix to a Pattern will reverse it.
>>> a = P[:4]
>>> print(a, ~a)
P[0, 1, 2, 3], P[3, 2, 1, 0]

##### `__iter__(self)`

Returns a generator object for this Pattern 

##### `__le__(self, other)`

Return self<=value.

##### `__len__(self)`

Returns the *expanded* length of the pattern such that if the pattern is laced, the
value is the length of the list multiplied by the lowest-common-multiple of the lengths
of nested patterns. e.g. the following are identical:
```
>>> print( len(P[0,1,2,[3,4]]) )
8
>>> print( len(P[0,1,2,3,0,1,2,4]) )
8
```

##### `__lt__(self, other)`

Return self<value.

##### `__ne__(self, other)`

Return self!=value.

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__repr__(self)`

Return repr(self).

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `__str__(self)`

Return str(self).

##### `accum(self, *args)`

Returns a Pattern that is equivalent to list of sums of that
Pattern up to that index.

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `arp(self, arp_pattern)`

Return a new Pattern with each item repeated len(arp_pattern) times
and incremented by arp_pattern. Useful for arpeggiating. e.g.
```
>>> P[0, 1, 2, 3].arp([0, 2])
P[0, 2, 1, 3, 2, 4, 3, 5]
```

##### `asGroup(self)`

Returns the Pattern as a PGroup 

##### `bubble(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `choose(self)`

Returns one randomly selected item 

##### `convert_data(self, dtype=<class 'float'>, *args, **kwargs)`

Makes a true copy and converts the data to a given data type 

##### `copy(self)`

Returns a copy of the Pattern such that alterations to the
Pattern.data do not affect the original.

##### `count(self, item)`

Returns the number of occurrences of item in the Pattern

##### `deep_shuffle(self, n=1)`

Returns a new Pattern with shuffled contents and shuffles
any nested patterns. To shuffle the contents of nested patterns
with the rest of the Pattern's contents, use `true_shuffle`.

##### `duplicate(self, *args)`

Repeats this pattern n times but keep nested pattern values 

##### `every(self, n, method, *args, **kwargs)`

Returns the pattern looped n-1 times then appended with
the version returned when method is called on it. 

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `getitem(self, key, *args)`

Called by __getitem__() 

##### `group(self)`

Returns the Pattern as a PGroup 

##### `help(cls)`

Prints the Pattern class docstring to the console 

##### `invert(self)`

Inverts the values with the Pattern.
        

##### `items(self)`

Returns a generator object equivalent to using enumerate() 

##### `iter(self, *args)`

Repeats this pattern n times but doesn't take nested pattern into account for length

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `limit(self, *args)`

Returns a new Pattern generated by adding elements from
this Pattern to a new list and repeatedly calling
`func()` on this list until `func(l)` is greater than `value`
e.g.
```
>>> print( P[0, 1, 2, 3].limit(sum, 10) )
P[0, 1, 2, 3, 0, 1, 2]
```

##### `loop(self, *args)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `map(self, func)`

Returns a Pattern that calls `func` on each item 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `norm(self)`

Returns the pattern with all values between 0 and 1 

##### `offlayer(self, dur, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `palindrome(self, *args)`

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

##### `pivot(self, *args)`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `reverse(self)`

Reverses the contents of the Pattern. Nested patterns are
not reversed. To reverse the contents of nester patterns
use `Pattern.mirror()`

##### `sample(self, *args)`

Returns an n-length pattern from a sample

##### `shuffle(self, n=1)`

Returns a new Pattern with shuffled contents. Note: nested patterns
stay together. To shuffle the contents of nested patterns, use
`deep_shuffle` or `true_shuffle`.

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

##### `startswith(self, prefix)`

Returns True if the first item in the Pattern is equal to prefix 

##### `stretch(self, *args)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `stutter(self, n=2)`

Returns a new Pattern with each item repeated by `n`. Use
a list of numbers for stutter different items by different
amount. e.g.
```
>>> P[0, 1, 2, 3].stutter([1,3])
P[0, 1, 1, 1, 2, 3, 3, 3]
```

##### `true_copy(self, new_data=None)`

Returns a copy of the Pattern such that items within the
Pattern hold the same state as the original.

##### `true_shuffle(self, n=1)`

Returns a new Pattern with completely shuffle contents such
that nested Patterns are shuffled within the larger Pattern

##### `undup(self)`

Removes any consecutive duplicate numbers from a Pattern 

##### `zip(self, other, dtype=None)`

Zips two patterns together. If one item is a tuple, it extends the tuple / PGroup
i.e. arrow_zip([(0,1),3], [2]) -> [(0,1,2),(3,2)]

##### `zipx(self, other)`

Returns a `Pattern` of `PGroups`, where each `PGroup` contains the i-th
element from each of the argument sequences. The length of the pattern
is the lowest common multiple of the lengths of the two joining patterns. 

---

### `metaPattern(self, data=[])`

Abstract base class for Patterns 

#### Methods

##### `__eq__(self, other)`

Return self==value.

##### `__ge__(self, other)`

Return self>=value.

##### `__getitem__(self, key)`

Overrides the Pattern.__getitem__ to allow indexing
by TimeVar and PlayerKey instances. 

##### `__gt__(self, other)`

Return self>value.

##### `__init__(self, data=[])`

Initialize self.  See help(type(self)) for accurate signature.

##### `__invert__(self)`

Using the ~ symbol as a prefix to a Pattern will reverse it.
>>> a = P[:4]
>>> print(a, ~a)
P[0, 1, 2, 3], P[3, 2, 1, 0]

##### `__iter__(self)`

Returns a generator object for this Pattern 

##### `__le__(self, other)`

Return self<=value.

##### `__len__(self)`

Returns the *expanded* length of the pattern such that if the pattern is laced, the
value is the length of the list multiplied by the lowest-common-multiple of the lengths
of nested patterns. e.g. the following are identical:
```
>>> print( len(P[0,1,2,[3,4]]) )
8
>>> print( len(P[0,1,2,3,0,1,2,4]) )
8
```

##### `__lt__(self, other)`

Return self<value.

##### `__ne__(self, other)`

Return self!=value.

##### `__or__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__repr__(self)`

Return repr(self).

##### `__ror__(self, other)`

Use the '|' symbol to 'pipe' Patterns into on another 

##### `__setslice__(self, i, j, item)`

Only works in Python 2 

##### `__str__(self)`

Return str(self).

##### `accum(self, *args)`

Returns a Pattern that is equivalent to list of sums of that
Pattern up to that index.

##### `all(self, func=<lambda>)`

Returns true if all of the patterns contents satisfies func(x) - default is nonzero 

##### `amen(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `arp(self, arp_pattern)`

Return a new Pattern with each item repeated len(arp_pattern) times
and incremented by arp_pattern. Useful for arpeggiating. e.g.
```
>>> P[0, 1, 2, 3].arp([0, 2])
P[0, 2, 1, 3, 2, 4, 3, 5]
```

##### `asGroup(self)`

Returns the Pattern as a PGroup 

##### `bubble(self, size=2)`

Merges and laces the first and last two items such that a
drum pattern "x-o-" would become "(x[xo])-o([-o]-)" 

##### `choose(self)`

Returns one randomly selected item 

##### `convert_data(self, dtype=<class 'float'>, *args, **kwargs)`

Makes a true copy and converts the data to a given data type 

##### `copy(self)`

Returns a copy of the Pattern such that alterations to the
Pattern.data do not affect the original.

##### `count(self, item)`

Returns the number of occurrences of item in the Pattern

##### `deep_shuffle(self, n=1)`

Returns a new Pattern with shuffled contents and shuffles
any nested patterns. To shuffle the contents of nested patterns
with the rest of the Pattern's contents, use `true_shuffle`.

##### `duplicate(self, *args)`

Repeats this pattern n times but keep nested pattern values 

##### `every(self, n, method, *args, **kwargs)`

Returns the pattern looped n-1 times then appended with
the version returned when method is called on it. 

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `getitem(self, key, get_generator=False)`

Called by __getitem__() 

##### `group(self)`

Returns the Pattern as a PGroup 

##### `help(cls)`

Prints the Pattern class docstring to the console 

##### `invert(self)`

Inverts the values with the Pattern.
        

##### `items(self)`

Returns a generator object equivalent to using enumerate() 

##### `iter(self, *args)`

Repeats this pattern n times but doesn't take nested pattern into account for length

##### `layer(self, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `limit(self, *args)`

Returns a new Pattern generated by adding elements from
this Pattern to a new list and repeatedly calling
`func()` on this list until `func(l)` is greater than `value`
e.g.
```
>>> print( P[0, 1, 2, 3].limit(sum, 10) )
P[0, 1, 2, 3, 0, 1, 2]
```

##### `loop(self, *args)`

Repeats this pattern n times 

##### `make(self)`

This method automatically laces and groups the data 

##### `map(self, func)`

Returns a Pattern that calls `func` on each item 

##### `mirror(self)`

Reverses the pattern. Differs to `Pattern.reverse()` in that
all nested patters are also reversed. 

##### `norm(self)`

Returns the pattern with all values between 0 and 1 

##### `offlayer(self, dur, method, *args, **kwargs)`

Zips a pattern with a modified version of itself. Method argument
can be a function that takes this pattern as its first argument,
or the name of a Pattern method as a string. 

##### `palindrome(self, *args)`

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

##### `pivot(self, *args)`

Mirrors and rotates the Pattern such that the item at index 'i'
is in the same place 

##### `replace(self, sub, repl)`

Replaces any occurrences of "sub" with "repl" 

##### `reverse(self)`

Reverses the contents of the Pattern. Nested patterns are
not reversed. To reverse the contents of nester patterns
use `Pattern.mirror()`

##### `sample(self, *args)`

Returns an n-length pattern from a sample

##### `shuffle(self, n=1)`

Returns a new Pattern with shuffled contents. Note: nested patterns
stay together. To shuffle the contents of nested patterns, use
`deep_shuffle` or `true_shuffle`.

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

##### `startswith(self, prefix)`

Returns True if the first item in the Pattern is equal to prefix 

##### `stretch(self, *args)`

Stretches (repeats) the contents until len(Pattern) == size 

##### `string(self)`

Returns a PlayString in string format from the Patterns values 

##### `stutter(self, n=2)`

Returns a new Pattern with each item repeated by `n`. Use
a list of numbers for stutter different items by different
amount. e.g.
```
>>> P[0, 1, 2, 3].stutter([1,3])
P[0, 1, 1, 1, 2, 3, 3, 3]
```

##### `true_copy(self, new_data=None)`

Returns a copy of the Pattern such that items within the
Pattern hold the same state as the original.

##### `true_shuffle(self, n=1)`

Returns a new Pattern with completely shuffle contents such
that nested Patterns are shuffled within the larger Pattern

##### `undup(self)`

Removes any consecutive duplicate numbers from a Pattern 

##### `zip(self, other, dtype=None)`

Zips two patterns together. If one item is a tuple, it extends the tuple / PGroup
i.e. arrow_zip([(0,1),3], [2]) -> [(0,1,2),(3,2)]

##### `zipx(self, other)`

Returns a `Pattern` of `PGroups`, where each `PGroup` contains the i-th
element from each of the argument sequences. The length of the pattern
is the lowest common multiple of the lengths of the two joining patterns. 

---

## Functions

### `ClassPatternMethod(f)`

Decorator that makes a function into a metaPattern class method

### `Convert(*args)`

Returns tuples/PGroups as PGroups, and anything else as Patterns 

### `Format(data)`

If data is a list, returns Pattern(data). If data is a tuple, returns PGroup(data).
Returns data if neither. 

### `PatternFormat(data)`

If data is a list, returns Pattern(data). If data is a tuple, returns PGroup(data).
Returns data if neither. 

### `PatternMethod(f)`

Decorator that makes a function into a metaPattern method

### `StaticPatternMethod(f)`

Decorator that makes a function into a metaPattern static  method

### `asPattern(item)`

None

### `asStream(data)`

Forces any data into a [pattern] form 

### `equal_values(this, that)`

Returns True if this == that 

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

