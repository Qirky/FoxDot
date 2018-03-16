# `Midi`

Module for converting handling MIDI in/out and functions relating to MIDI pitch calculation. 

## Classes

### `MIDIDeviceNotFound(self, *args, **kwargs)`

Common base class for all non-exit exceptions.

#### Methods

##### `__str__(self)`

Return str(self).

---

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



#### Methods

##### `__init__(self, degree=0, **kwargs)`

Initialize self.  See help(type(self)) for accurate signature.

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

### `_log2(num)`

None

### `freqtomidi(freq)`

None

### `midi(scale, octave, degree, root=0, stepsPerOctave=12)`

Calculates a midinote from a scale, octave, degree, and root 

### `midi2cps(midinote)`

Converts a midi number to frequency 

### `miditofreq(midinote)`

Converts a midi number to frequency 

## Data

