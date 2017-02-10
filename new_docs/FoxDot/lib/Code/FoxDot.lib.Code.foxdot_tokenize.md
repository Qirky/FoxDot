# `FoxDot.lib.Code.foxdot_tokenize`

Code to allow Python files written in FoxDot to account for the "when"
statements. These files are given a header of `# coding: FoxDot` and
should then be automatically tokenized.

Source: http://stackoverflow.com/questions/214881/can-you-add-new-statements-to-pythons-syntax

## Classes

### `StreamReader(self, *args, **kwargs)`



#### Methods

##### `read(self, size=-1, chars=-1, firstline=False)`

Decodes data from the stream self.stream and returns the
resulting object.

chars indicates the number of characters to read from the
stream. read() will never return more than chars
characters, but it might return less, if there are not enough
characters available.

size indicates the approximate maximum number of bytes to
read from the stream for decoding purposes. The decoder
can modify this setting as appropriate. The default value
-1 indicates to read and decode as much as possible.  size
is intended to prevent having to decode huge files in one
step.

If firstline is true, and a UnicodeDecodeError happens
after the first line terminator in the input only the first line
will be returned, the rest of the input will be kept until the
next call to read().

The method should use a greedy read strategy meaning that
it should read as much data as is allowed within the
definition of the encoding and the given size, e.g.  if
optional encoding endings or state markers are available
on the stream, these should be read too.

##### `next(self)`

Return the next decoded line from the input stream.

##### `readline(self, size=None, keepends=True)`

Read one line from the input stream and return the
decoded data.

size, if given, is passed as size argument to the
read() method.

##### `__getattr__(self, name, getattr=<built-in function getattr>)`

Inherit all other methods from the underlying stream.
        

##### `reset(self)`

Resets the codec buffers used for keeping state.

Note that no stream repositioning should take place.
This method is primarily intended to be able to recover
from decoding errors.

##### `seek(self, offset, whence=0)`

Set the input stream's current position.

Resets the codec buffers used for keeping state.

##### `encode(self, input, errors=strict)`

Encodes the object input and returns a tuple (output
object, length consumed).

errors defines the error handling to apply. It defaults to
'strict' handling.

The method may not store state in the Codec instance. Use
StreamCodec for codecs which have to keep state in order to
make encoding/decoding efficient.

The encoder must be able to handle zero length input and
return an empty object of the output object type in this
situation.

##### `readlines(self, sizehint=None, keepends=True)`

Read all lines available on the input stream
and return them as list of lines.

Line breaks are implemented using the codec's decoder
method and are included in the list entries.

sizehint, if given, is ignored since there is no efficient
way to finding the true end-of-line.

---

## Functions

### `_import(filename)`

Returns a 'translated' version of a Python file into FoxDot as a module  

### `_test(filename)`

Prints out the converted contents of a file 

### `read(file)`

Converts a file-like object into FoxDot code 

### `search_function(s)`

Allows "FoxDot" files to be imported properly 

### `translate(readline)`

Searches for any FoxDot syntax (currently only when statements) 

## Data

