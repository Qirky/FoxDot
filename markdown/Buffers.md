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

##### `__init__(self, fn, number, channels=1)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

---

### `BufferManager(self, server=FoxDot ServerManager Instance -> localhost:57110, paths=())`



#### Methods

##### `__init__(self, server=FoxDot ServerManager Instance -> localhost:57110, paths=())`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

##### `__str__(self)`

Return str(self).

##### `_allocateAndLoad(self, filename)`

Allocates and loads a buffer from a filename, with caching 

##### `_findSample(*args, **kwargs)`

Find a sample from a filename or pattern

Will first attempt to find an exact match (by abspath or relative to
the search paths). Then will attempt to pattern match in search paths.

##### `_getFileInDir(self, dirname, index)`

Return nth sample in a directory 

##### `_getNextBufnum(self)`

Get the next free buffer number 

##### `_getSoundFile(self, filename)`

Look for a file with all possible extensions 

##### `_getSoundFileOrDir(self, filename)`

Get a matching sound file or directory 

##### `_patternSearch(self, filename, index)`

Return nth sample that matches a path pattern

Path pattern is a relative path that can contain wildcards such as *
and ? (see fnmatch for more details). Some example paths:

    samp*
    **/voices/*
    perc*/bass*

##### `_searchPaths(self, filename)`

Search our search paths for an audio file or directory 

##### `addPath(self, path)`

Add a path to the search paths for samples 

##### `free(self, filenameOrBuf)`

Free a buffer. Accepts a filename or buffer number 

##### `freeAll(self)`

Free all buffers 

##### `getBuffer(self, bufnum)`

Get buffer information from the buffer number 

##### `getBufferFromSymbol(self, symbol, index=0)`

Get buffer information from a symbol 

##### `loadBuffer(self, filename, index=0)`

Load a sample and return the number of a buffer 

##### `setMaxBuffers(self, max_buffers)`

Set the max buffers on the SC server 

---

### `LoopSynthDef(self)`



#### Methods

##### `__call__(self, filename, pos=0, sample=0, **kwargs)`

Call self as a function.

##### `__getattribute__(self, key)`

Return getattr(self, name).

##### `__init__(self)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

##### `__setattr__(self, key, value)`

Implement setattr(self, name, value).

##### `__str__(self)`

Return str(self).

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

### `symbolToDir(symbol)`

Return the sample search directory for a symbol 

### `hasext(filename)`

None

## Data

#### `nil = <Buffer num 0>`

#### `Samples = <BufferManager>`

#### `loop = loop`

