# `Generators`

This module contains all the sub-classes of `GeneratorPattern` used in FoxDot. Unlike
a `Pattern`, a `GeneratorPattern` does not contain a list that is iterated over or
indexed but returns a value based on the index and an internal function. For example,
`PRand` returns a random value from a list of values. It will always return the same
value for the same index as it stores this in its internal cache. `Pattern` methods
such as `rotate` or `palindrome` are not available from the `GeneratorPattern` class
but slicing generators will return a `Pattern` object from which these methods can
be called e.g.

    >>> gen = PRand([0,1,2])
    >>> pat = gen[:5]
    P[0, 1, 0, 2, 1]
    >>> pat.rotate()
    P[1, 0, 2, 1, 0]

Mathematical operations *do* work in the same way as they do in `Patterns`.

    >>> gen1 = PRand([0,1,2])
    >>> gen2 = gen1 + 10
    >>> gen1[:5]
    P[0, 2, 2, 1, 0]
    >>> gen2[:5]
    P[10, 12, 12, 11, 10]

## Classes

### `PRand(self, start, stop=None, **kwargs)`

Returns a random integer between start and stop. If start is a container-type it returns
a random item for that container. 

#### Methods

##### `__init__(self, start, stop=None, **kwargs)`

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

##### `string(self)`

Used in PlayString to show a PRand in curly braces 

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

### `PxRand(self, start, stop=None, **kwargs)`

Returns a random integer between start and stop. If start is a container-type it returns
a random item for that container. 

#### Methods

##### `__init__(self, start, stop=None, **kwargs)`

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

##### `string(self)`

Used in PlayString to show a PRand in curly braces 

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

### `PwRand(self, values, weights, **kwargs)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

##### `__init__(self, values, weights, **kwargs)`

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

### `PChain(self, mapping, **kwargs)`

An example of a Markov Chain generator pattern. The mapping argument 
should be a dictionary of keys whose values are a list/pattern of possible
destinations.  

#### Methods

##### `__init__(self, mapping, **kwargs)`

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

### `PZ12(self, p, tokens=[0, 1])`

Implementation of the PZ12 algorithm for predetermined random numbers. Using
an irrational value for p, however, results in a non-determined order of values. 

#### Methods

##### `__init__(self, p, tokens=[0, 1])`

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

### `PTree(self, n=0, f=<lambda>, choose=<lambda>, **kwargs)`

Takes a starting value and two functions as arguments. The first function, f, must
take one value and return a container-type of values and the second function, choose,
must take a container-type and return a single value. In essence you are creating a
tree based on the f(n) where n is the last value chosen by choose.

#### Methods

##### `__init__(self, n=0, f=<lambda>, choose=<lambda>, **kwargs)`

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

### `PWalk(self, max=7, step=1, start=0, **kwargs)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

##### `__init__(self, max=7, step=1, start=0, **kwargs)`

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

### `PWhite(self, lo=0, hi=1, **kwargs)`

Returns random floating point values between 'lo' and 'hi' 

#### Methods

##### `__init__(self, lo=0, hi=1, **kwargs)`

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

### `PSquare(self, **kwargs)`

Returns the square of the index being accessed 

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

### `PIndex(self, **kwargs)`

Returns the index being accessed 

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

### `PFibMod(self, **kwargs)`

Returns the fibonacci sequence -- maybe a bad idea

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

## Functions

## Data

