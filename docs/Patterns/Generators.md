# `Generators`

## Classes

### `PChain(self, mapping, **kwargs)`



#### Methods

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

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

### `PRand(self, start, stop=None, **kwargs)`

Returns a random integer between start and stop. If start is a container-type it returns
a random item for that container. 

#### Methods

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

##### `string(self)`

Used in PlayString to show a PRand in curly braces 

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

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

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

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

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



#### Methods

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

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

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

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



#### Methods

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

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



#### Methods

##### `__repr__(self)`

String version is the name of the class and its arguments 

##### `_randbelow(self, n, _log=<built-in function log>, _int=<type 'int'>, _maxwidth=9007199254740992, _Method=<type 'instancemethod'>, _BuiltinMethod=<type 'builtin_function_or_method'>)`

Return a random int in the range [0,n)

Handles the case where n has more bits than returned
by a single call to the underlying generator.

##### `betavariate(self, alpha, beta)`

Beta distribution.

Conditions on the parameters are alpha > 0 and beta > 0.
Returned values range between 0 and 1.

##### `choice(self, seq)`

Choose a random element from a non-empty sequence.

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

##### `getitem(self, index=None)`

Calls self.func(index) to get an item if index is not in
self.history, otherwise returns self.history[index] 

##### `getstate(self)`

Return internal state; can be passed to setstate() later.

##### `jumpahead(self, n)`

Change the internal state to one that is likely far away
from the current state.  This method will not be in Py3.x,
so it is better to simply reseed.

##### `lognormvariate(self, mu, sigma)`

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a
normal distribution with mean mu and standard deviation sigma.
mu can have any value, and sigma must be greater than zero.

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
        

##### `randrange(self, start, stop=None, step=1, _int=<type 'int'>, _maxwidth=9007199254740992)`

Choose a random item from range(start, stop[, step]).

This fixes the problem with randint() which includes the
endpoint; in Python this is usually not what you want.

##### `sample(self, population, k)`

Chooses k unique random elements from a population sequence.

Returns a new list containing elements from the population while
leaving the original population unchanged.  The resulting list is
in selection order so that all sub-slices will also be valid random
samples.  This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the population need not be hashable or unique.  If the
population contains repeats, then each occurrence is a possible
selection in the sample.

To choose a sample in a range of integers, use xrange as an argument.
This is especially fast and space efficient for sampling from a
large population:   sample(xrange(10000000), 60)

##### `seed(self, a=None)`

Initialize internal state from hashable object.

None or no argument seeds from current time or from an operating
system specific randomness source if available.

If a is not None or an int or long, hash(a) is used instead.

##### `setstate(self, state)`

Restore internal state from object returned by getstate().

##### `shuffle(self, x, random=None)`

x, random=random.random -> shuffle list x in place; return None.

Optional arg random is a 0-argument function returning a random
float in [0.0, 1.0); by default, the standard random.random.

##### `string(self)`

Used in PlayString to show a PRand in curly braces 

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

