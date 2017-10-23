# `Midi`

Module for converting streams and frequencies 

## Classes

### `MIDIDeviceNotFound(self)`



#### Methods

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

---

### `rtMidiNotFound(self)`



#### Methods

---

## Functions

### `midi(scale, octave, degree, root=0, stepsPerOctave=12)`

Calculates a midinote from a scale, octave, degree, and root 

### `midi2cps(midinote)`

Converts a midi number to frequency 

### `miditofreq(midinote)`

Converts a midi number to frequency 

## Data

