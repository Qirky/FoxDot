# `Midi`

Module for converting handling MIDI in/out and functions relating to MIDI pitch calculation. 

## Classes

### `MidiIn(self, port_id=0)`



#### Methods

##### `__init__(self, port_id=0)`

Class for listening for MIDI clock messages
from a midi device 

##### `close(self)`

Closes the active port 

##### `get_beat(self)`

If a beat value has been set, return it, otherwise return None 

---

### `MidiOut(self, degree=0, **kwargs)`

SynthDef proxy for sending midi message via supercollider 

#### Methods

##### `__init__(self, degree=0, **kwargs)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__str__(self)`

Return str(self).

---

### `MIDIDeviceNotFound(self, *args, **kwargs)`

Common base class for all non-exit exceptions.

#### Methods

##### `__str__(self)`

Return str(self).

---

### `rtMidiNotFound(self, *args, **kwargs)`

Common base class for all non-exit exceptions.

#### Methods

##### `__str__(self)`

Return str(self).

---

## Functions

## Data

