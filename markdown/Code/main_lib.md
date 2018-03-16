# `main_lib`

## Classes

### `CodeString(self, raw)`



#### Methods

---

### `FoxDotCode(self, *args, **kwargs)`



#### Methods

---

### `LiveObject(self, *args, **kwargs)`



#### Methods

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

