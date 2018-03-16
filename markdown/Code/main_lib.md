# `main_lib`

## Classes

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

### `LiveObject(self, *args, **kwargs)`



#### Methods

##### `__call__(self)`

Call self as a function.

---

## Functions

### `WarningMsg(*text)`

None

### `classes(module)`

Returns a list of class names defined in module 

### `clean(string)`

None

### `debug_stdout(*args)`

Forces prints to server-side 

### `functions(module)`

Returns a list of function names defined in module 

### `get_input()`

Similar to `input` but can handle multi-line input. Terminates on a final "
" 

### `get_now(obj)`

Returns the value of objects if they are time-varying 

### `handle_stdin()`

When FoxDot is run with the --pipe added, this function
is called and continuosly   

### `instances(module, cls)`

Returns a list of instances of cls from module 

### `stdout(code)`

Shell-based output 

### `write_to_file(fn, text)`

None

## Data

#### `execute = <FoxDot.lib.Code.main_lib.FoxDotCode object>`

