# `main_lib`

## Classes

### `LiveObject(self, *args, **kwargs)`



#### Methods

##### `__call__(self)`

Call self as a function.

---

### `CodeString(self, raw)`



#### Methods

##### `__init__(self, raw)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__str__(self)`

Return str(self).

---

### `FoxDotCode(self, *args, **kwargs)`



#### Methods

##### `__call__(self, code, verbose=True, verbose_error=None)`

Takes a string of FoxDot code and executes as Python 

##### `_compile(string)`

Returns the bytecode for  

---

## Functions

### `clean(string)`

None

### `get_now(obj)`

Returns the value of objects if they are time-varying 

### `get_input()`

Similar to `input` but can handle multi-line input. Terminates on a final "
" 

### `handle_stdin()`

When FoxDot is run with the --pipe added, this function
is called and continuosly   

### `stdout(code)`

Shell-based output 

### `debug_stdout(*args)`

Forces prints to server-side 

### `WarningMsg(*text)`

None

### `write_to_file(fn, text)`

None

### `classes(module)`

Returns a list of class names defined in module 

### `instances(module, cls)`

Returns a list of instances of cls from module 

### `functions(module)`

Returns a list of function names defined in module 

## Data

#### `execute = <FoxDot.lib.Code.main_lib.FoxDotCode object>`

