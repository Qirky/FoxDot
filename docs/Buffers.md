# `Buffers`

This module manages the allocation of buffer numbers and samples. To see
a list of descriptions of what sounds are mapped to what characters,
simply evaluate

    print(Samples)

Future:

Aiming on being able to set individual sample banks for different players
that can be proggrammed into performance.

## Classes

### `BufChar(self, char)`



#### Methods

---

### `Buffer(self, fn, number, channels=1)`



#### Methods

---

### `BufferManager(self)`



#### Methods

---

### `LoopFile(self, char)`



#### Methods

---

### `LoopSynthDef(self)`



#### Methods

##### `add(self)`

This is required to add the SynthDef to the SuperCollider Server 

##### `add_base_class_behaviour(self)`

Defines the initial setup for every SynthDef 

##### `play(self, freq, **kwargs)`

Plays a single sound 

##### `write(self)`

Writes the SynthDef to file 

---

## Functions

### `FindBuffer(name)`

None

### `path(fn)`

None

## Data

#### `Samples = <FoxDot.lib.Buffers.BufferManager instance>`

#### `loop = loop`

