# `FoxDot.lib.Buffers`

This module manages the allocation of buffer numbers and samples 

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

