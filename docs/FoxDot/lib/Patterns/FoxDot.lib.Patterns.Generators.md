# `FoxDot.lib.Patterns.Generators`

None

## Classes

### `PChain(self, mapping)`



#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PRand(self, start, stop=None)`

Returns a random integer between start and stop. If start is a container-type it returns
a random item for that container. 

#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

##### `string(self)`

Used in PlayString to show a PRand in curly braces 

---

### `PSquare(self)`

Returns the square of the index being accessed 

#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PTree(self, n=0, f=<lambda>, choose=<lambda>)`

Takes a starting value and two functions as arguments. The first function, f, must
take one value and return a container-type of values and the second function, choose,
must take a container-type and return a single value. In essence you are creating a
tree based on the f(n) where n is the last value chosen by choose.

#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PWalk(self, max=7, step=1, start=0)`



#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PWhite(self, lo=0, hi=1)`

Returns random floating point values between 'lo' and 'hi' 

#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PwRand(self, values, weights)`



#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

---

### `PxRand(self, start, stop=None)`



#### Methods

##### `getitem(self, index=None)`

Calls self.func(index) to get an item, and also calculates
performs any arithmetic operation assigned 

##### `string(self)`

Used in PlayString to show a PRand in curly braces 

---

## Functions

## Data

