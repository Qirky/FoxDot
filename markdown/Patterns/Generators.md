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

### `PChain(self, mapping, **kwargs)`

An example of a Markov Chain generator pattern. The mapping argument 
should be a dictionary of keys whose values are a list/pattern of possible
destinations.  

#### Methods

---

### `PFibMod(self, **kwargs)`

Returns the fibonacci sequence -- maybe a bad idea

#### Methods

---

### `PIndex(self, **kwargs)`

Returns the index being accessed 

#### Methods

---

### `PRand(self, start, stop=None, **kwargs)`

Returns a random integer between start and stop. If start is a container-type it returns
a random item for that container. 

#### Methods

---

### `PSquare(self, **kwargs)`

Returns the square of the index being accessed 

#### Methods

---

### `PTree(self, n=0, f=<lambda>, choose=<lambda>, **kwargs)`

Takes a starting value and two functions as arguments. The first function, f, must
take one value and return a container-type of values and the second function, choose,
must take a container-type and return a single value. In essence you are creating a
tree based on the f(n) where n is the last value chosen by choose.

#### Methods

---

### `PWalk(self, max=7, step=1, start=0, **kwargs)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

---

### `PWhite(self, lo=0, hi=1, **kwargs)`

Returns random floating point values between 'lo' and 'hi' 

#### Methods

---

### `PZ12(self, p, tokens=[0, 1])`

Implementation of the PZ12 algorithm for predetermined random numbers. Using
an irrational value for p, however, results in a non-determined order of values. 

#### Methods

---

### `PwRand(self, values, weights, **kwargs)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

---

### `PxRand(self, start, stop=None, **kwargs)`

Returns a random integer between start and stop. If start is a container-type it returns
a random item for that container. 

#### Methods

---

## Functions

## Data

