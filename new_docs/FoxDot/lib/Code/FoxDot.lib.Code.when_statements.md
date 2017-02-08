# FoxDot.lib.Code.when_statements

None

## Classes

### `_whenLibrary(self)`

#### Methods

##### `run(self)`

Continual loop evaluating when_statements
        

##### `reset(self)`

Clears the library and stop scheduling 

##### `__call__(self, func=None, **kwargs)`

Calling when() with no arguments will evaluate all expressions
stored in self.library. Calling with func as a valid function
will see if the function is in self.library and add it if not,
or update the 

---

### `_whenStatement(self, func)`

#### Methods

##### `toggle_live_functions(self, switch)`

If the action functions are @livefunctions, turn them on/off 

---

## Functions

## Data

### `when`

Example:

A. when(lambda: x==10).do(lambda: p.shuffle()).elsedo(lambda: p. reverse())

