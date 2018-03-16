# `Midi`

Module for converting handling MIDI in/out and functions relating to MIDI pitch calculation. 

## Classes

### `MIDIDeviceNotFound(self, *args, **kwargs)`

Common base class for all non-exit exceptions.

#### Methods

---

### `MidiIn(self, port_id=0)`



#### Methods

---

### `MidiOut(self, degree=0, **kwargs)`



#### Methods

---

### `rtMidiNotFound(self, *args, **kwargs)`

Common base class for all non-exit exceptions.

#### Methods

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

