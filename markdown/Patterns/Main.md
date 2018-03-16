# `Main`

Contains classes `Pattern` and `PGroup` and the base class for `GeneratorPattern` (see Generators.py).

## Classes

### `EmptyItem(self)`

Can be used in a pattern and and is essentially not there 

#### Methods

---

### `GeneratorPattern(self, **kwargs)`

Used for when a Pattern does not generate a set length pattern,
e.g. random patterns

#### Methods

---

### `PGroup(self, seq=[], *args)`

Class to represent any groupings of notes as denoted by brackets.
PGroups should only be found within a Pattern object.

#### Methods

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `help(cls)`

Prints the Pattern class docstring to the console 

---

### `Pattern(self, data=[])`

Base type pattern 

#### Methods

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `help(cls)`

Prints the Pattern class docstring to the console 

---

### `PatternContainer(self, data=[])`

Abstract base class for Patterns 

#### Methods

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `help(cls)`

Prints the Pattern class docstring to the console 

---

### `metaPattern(self, data=[])`

Abstract base class for Patterns 

#### Methods

##### `get_methods(cls)`

Returns the methods associated with the `Pattern` class as a list 

##### `help(cls)`

Prints the Pattern class docstring to the console 

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

