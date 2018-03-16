# `Repeat`

## Classes

### `MethodList(self, root)`

Class for holding information about the order of which methods have been
called on Player attributes. `root` is the original Pattern.

#### Methods

##### `__contains__(self, method)`

Returns true if the method is in the list of methods 

##### `__init__(self, root)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

##### `remove(self, method)`

Removes a method (should be a string) from the list of methods 

##### `update(self, method, args, kwargs)`

Updates the args and kwargs for a repeated method 

---

### `Repeatable(self)`



#### Methods

##### `__init__(self)`

Initialize self.  See help(type(self)) for accurate signature.

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in 'n' beats time
```
# Stop the player looping after 16 beats
p1 >> pads().after(16, "stop")
```

##### `every(self, occurence, cmd, *args, **kwargs)`

Every n beats, call a method (defined as a string) on the
object and use the args and kwargs. To call the method
every n-th beat of a timeframe, use the `cycle` keyword argument
to specify that timeframe.

::
    # Call the shuffle method every 4 beats

    p1.every(4, 'shuffle')

    # Call the stutter method on the 5th beat of every 8 beat cycle

    p1.every(5, 'stutter', 4, cycle=8)

    # If the method is not valid but *is* a valid Pattern method, that is called and reverted

    p1.every(4, 'palindrome')

##### `get_attr_and_method_name(self, cmd)`

Returns the attribute and method name from a string in the form
`"attr.method"` would return `"attr"` and `"method"`. If attr is not
present, it returns `"degree"` in place. 

##### `get_method_by_name(self, cmd)`

Returns the attribute name and method based on `cmd` which is a string.
Should be in form `"attr.method"`.

##### `is_pattern_method(self, method_name, attr=degree)`

Returns True if the method is a valid method of `Pattern` 

##### `is_player_method(self, method_name, attr=degree)`

Returns True if the method is a valid method  of `Player` 

##### `never(self, cmd, ident=None)`

Stops calling cmd on repeat 

##### `stop_calling_all(self)`

Stops all repeated methods. 

##### `update_pattern_methods(self, attr)`

Update the 'current' version of a pattern based on its root and methods stored 

##### `update_pattern_root(self, attr)`

Update the base attribute pattern that methods are applied to 

---

### `MethodCall(self, parent, method, n, cycle=None, args=(), kwargs={})`

Class to represent an object's method call that,
when called, schedules itself in the future 

#### Methods

##### `__call__(self, *args, **kwargs)`

Proxy for parent object __call__, calls the enclosed method and schedules it in the future. 

##### `__init__(self, parent, method, n, cycle=None, args=(), kwargs={})`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

##### `call_method(self)`

Calls the method. Prints to the console with error info. 

##### `count(self)`

Counts the number of times this method would have been called between clock start and now 

##### `isScheduled(self)`

Returns True if this is in the Tempo Clock 

##### `schedule(self)`

Schedules the method to be called in the clock 

##### `update(self, n, cycle=None, args=(), kwargs={})`

Updates the values of the MethodCall. Re-adjusts the index if cycle has been changed 

---

## Functions

## Data

