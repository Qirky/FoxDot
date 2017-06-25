# `FoxDot.lib.Effects`

None

## Classes

### `Effect(self, foxdot_name, synthdef, args=[])`



#### Methods

##### `save(self)`

writes to file and sends to server 

---

### `EffectManager(self)`



#### Methods

##### `all_kwargs(self)`

Returns *all" keywords for all effects 

##### `kwargs(self)`

Returns the title keywords for each effect 

---

### `Out(self)`



#### Methods

##### `save(self)`

writes to file and sends to server 

---

### `PreEffect(self, *args, **kwargs)`

SynthDef that modulates argumentes such as frequency
*before* being used in a UGen. 

#### Methods

##### `save(self)`

writes to file and sends to server 

---

## Functions

## Data

#### `FxList = {'formant': <Fx 'formantFilter' -- args: formant...>, 'hpf': <Fx 'highPassFilter' -- args: hpf,hpr>}`

#### `fx = <Fx 'wavesShapeDistortion' -- args: shape>`

