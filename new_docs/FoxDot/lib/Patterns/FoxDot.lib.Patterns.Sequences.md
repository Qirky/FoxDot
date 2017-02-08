# FoxDot.lib.Patterns.Sequences

Sequences.py
------------
All patterns inherit from Base.Pattern. There are two types of pattern:

1. Container types
    - Similar to lists but with different mathematical operators
2. Generator types
    - Similar to generators but can be indexed (returns values based on functions)

## Classes

### `PRand(self, start, stop=None)`

#### Methods

##### `getitem(self, index)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PSquare(self)`

#### Methods

##### `getitem(self, index)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PWhite(self, lo=0, hi=1)`

#### Methods

##### `getitem(self, index)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PwRand(self)`

#### Methods

##### `getitem(self, index)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

## Functions

### `PAlt(pat1, pat2, *patN)`

None

### `PPairs(seq, func=<lambda>)`

PPairs(iterable, func=lambda n: 8-n)

Laces a sequence with a second sequence obtained
by performing a function on the original 

### `PShuf(seq)`

PShuf(seq) -> Returns a shuffled version of seq

### `PStretch(seq, size)`

None

### `PStutter(seq, n=2)`

PStutter(seq, n) -> Creates a pattern such that each item in the array is repeated n times (n can be a pattern) 

### `PZip(pat1, pat2, *patN)`

None

### `PZip2(pat1, pat2, rule=<lambda>)`

None

### `loop_pattern_func(f)`

Wrapper for allowing any Pattern function to create
multiple Patterns by using Patterns as arguments 

### `new_function(*args)`

None

## Data

### `P`

Pseudo-pattern.
P[1,2,3] = Pattern([1,2,3])
P(1,2,3) = Pattern((0,1,3))

### `R`

Pseudo-RandomGenerator.
R[1,2,3]

