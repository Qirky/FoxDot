# `FoxDot.lib.Repeat`

Repeat.py 

## Classes

### `MethodCall(self, parent, method, n, args=(), kwargs={})`

Class to represent an object's method call that,
when called, schedules itself in the future 

#### Methods

##### `__call__(self)`

Proxy for parent object __call__ 

##### `isScheduled(self)`

Returns True if this is in the Tempo Clock 

---

### `Repeatable(self)`



#### Methods

##### `whenmod(self, mod, n, cmd, *args, **kwargs)`

Every n beats, do self.cmd(args) 

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in n beats 

##### `every(self, n, cmd, *args, **kwargs)`

Every n beats, do self.cmd(args) 

---

### `WhenModMethodCall(self, parent, method, mod, n, args=(), kwargs={})`



#### Methods

##### `__call__(self)`

Proxy for parent object __call__ 

##### `isScheduled(self)`

Returns True if this is in the Tempo Clock 

---

## Functions

## Data

