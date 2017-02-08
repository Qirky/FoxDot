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

### `P10(n)`

None

### `PAlt(pat1, pat2, *patN)`

None

### `PDur(n, k, dur=0.25)`

Returns the *actual* durations based on Euclidean rhythms (see PEuclid) where dur
is the length of each step.
e.g. PDur(3, 8) -> P[0.75, 0.75, 0.5] 

### `PEuclid(n, k)`

Returns the Euclidean rhythm which spreads 'n' pulses over 'k' steps as evenly as possible.
e.g. PEuclid(3, 8) -> P[1, 0, 0, 1, 0, 0, 1, 0] 

### `PPairs(seq, func=<lambda>)`

PPairs(iterable, func=lambda n: 8-n)

Laces a sequence with a second sequence obtained
by performing a function on the original 

### `PRange(start, stop=None, step=None)`

None

### `PShuf(seq)`

PShuf(seq) -> Returns a shuffled version of seq

### `PSine(n=16)`

Returns values of one cycle of sine wave split into 'n' parts 

### `PSq(a=1, b=2, c=3)`

None

### `PStep(n, value, default=0)`

None

### `PStretch(seq, size)`

None

### `PStutter(seq, n=2)`

PStutter(seq, n) -> Creates a pattern such that each item in the array is repeated n times (n can be a pattern) 

### `PSum(n, total, **kwargs)`

PSum(n, total) -> Pattern of length n that sums to equal total

e.g. PSum(3,8) -> [3,3,2]
     PSum(5,4) -> [1,0.75,0.75,0.75,0.75]

### `PTri(start, stop=None, step=None)`

None

### `PZip(pat1, pat2, *patN)`

None

### `PZip2(pat1, pat2, rule=<lambda>)`

None

### `loop_pattern_func(f)`

Wrapper for allowing any Pattern function to create
multiple Patterns by using Patterns as arguments 

## Data

### `P`

Pseudo-pattern.
P[1,2,3] = Pattern([1,2,3])
P(1,2,3) = Pattern((0,1,3))

### `R`

Pseudo-RandomGenerator.
R[1,2,3]

