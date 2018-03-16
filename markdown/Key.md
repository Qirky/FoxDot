# `Key`

## Classes

### `Accompany(self, freq=0, rel=[0, 2, 4])`

Like PlayerKey except it returns 

#### Methods

##### `__call__(self, playerkey)`

Acts as a function in Player Key 

##### `__init__(self, freq=0, rel=[0, 2, 4])`

Initialize self.  See help(type(self)) for accurate signature.

---

### `NumberKey(self, value, reference)`



#### Methods

##### `__add__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__eq__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ge__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__gt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__init__(self, value, reference)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__le__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__lt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ne__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__pow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__radd__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__repr__(self)`

Return repr(self).

##### `__rfloordiv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rpow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rsub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rtruediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rxor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__str__(self)`

Return str(self).

##### `__sub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__truediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__xor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `accompany(self, freq=0, rel=[0, 2, 4])`

Returns a PlayerKey whose function returns an accompanying note 

##### `index(self, sequence)`

Returns a Player Key that returns the element from sequence indexed using int(self) 

##### `map(self, mapping, default=0)`

Allows for functional mapping. `mapping` is a dictionary of keys, which can
be functions, and values, which can also be functions. If neither is callable,
then the the mapping function returns the value when this Player Key  is equal
to the key. The key can be callable and will return the value provided if the
the callable key function returns True (it must take one argument, this Player Key).
Trivially, the following mappings are equivalent in behaviour:

::
    p1 >> piano(p2.degree.map({4: 7}))

    p1 >> piano(p2.degree.map({lambda x: x == 4: 7}))

If the value is callable, then it is called on this player key when the key
is satisfied:

::
    p1 >> piano(p2.degree.map({lambda x: x >= 4: lambda x: x + (0,2)}))

##### `now(self, other=None)`

Returns the current value in the Key by calling the parent 

##### `semitones(self)`

Converts the current value into the semitone value using the parent's scale 

##### `simple_map(self, mapping)`

Creates a new Player key that maps the values in the dictionary (mapping)
to new values. Example use case:

```
d1 >> play("x-o-", sample=d1.degree.simple_map( { "-" : -1, "o" : var([0,2]) }))
```

##### `transform(self, func)`

Returns a child Player Key based on the func 

---

### `PlayerKey(self, value=None, reference=None, parent=None, attr=None)`



#### Methods

##### `__add__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__eq__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ge__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__gt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__init__(self, value=None, reference=None, parent=None, attr=None)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__le__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__lt__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__mul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__ne__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__pow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__radd__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__repr__(self)`

Return repr(self).

##### `__rfloordiv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmod__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rmul__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rpow__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rsub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rtruediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__rxor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__str__(self)`

Return str(self).

##### `__sub__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__truediv__(self, other)`

If operating with a pattern, return a pattern of values 

##### `__xor__(self, other)`

If operating with a pattern, return a pattern of values 

##### `accompany(self, freq=0, rel=[0, 2, 4])`

Returns a PlayerKey whose function returns an accompanying note 

##### `index(self, sequence)`

Returns a Player Key that returns the element from sequence indexed using int(self) 

##### `map(self, mapping, default=0)`

Allows for functional mapping. `mapping` is a dictionary of keys, which can
be functions, and values, which can also be functions. If neither is callable,
then the the mapping function returns the value when this Player Key  is equal
to the key. The key can be callable and will return the value provided if the
the callable key function returns True (it must take one argument, this Player Key).
Trivially, the following mappings are equivalent in behaviour:

::
    p1 >> piano(p2.degree.map({4: 7}))

    p1 >> piano(p2.degree.map({lambda x: x == 4: 7}))

If the value is callable, then it is called on this player key when the key
is satisfied:

::
    p1 >> piano(p2.degree.map({lambda x: x >= 4: lambda x: x + (0,2)}))

##### `now(self, other=None)`

Returns the current value in the Key by calling the parent 

##### `semitones(self)`

Converts the current value into the semitone value using the parent's scale 

##### `simple_map(self, mapping)`

Creates a new Player key that maps the values in the dictionary (mapping)
to new values. Example use case:

```
d1 >> play("x-o-", sample=d1.degree.simple_map( { "-" : -1, "o" : var([0,2]) }))
```

##### `transform(self, func)`

Returns a child Player Key based on the func 

##### `update(self, value, time)`

Updates the contents of the PlayerKey *if* the time value is different to self.last_updated.
If they are the same, the the contents become a PGroup of the two values 

---

## Functions

## Data

