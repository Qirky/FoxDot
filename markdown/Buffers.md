# `Buffers`

This module manages the allocation of buffer numbers and samples. To see
a list of descriptions of what sounds are mapped to what characters,
simply evaluate

    print(Samples)

Future:

Aiming on being able to set individual sample banks for different players
that can be proggrammed into performance.

## Classes

### `Buffer(self, fn, number, channels=1)`



#### Methods

---

### `BufferManager(self, server=FoxDot ServerManager Instance -> localhost:57110, paths=())`



#### Methods

---

### `LoopSynthDef(self)`



#### Methods

---

## Functions

### `hasext(filename)`

None

### `symbolToDir(symbol)`

Return the sample search directory for a symbol 

## Data

#### `Samples = <BufferManager>`

#### `loop = loop`

#### `nil = <Buffer num 0>`

