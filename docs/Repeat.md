# `Repeat`

## Classes

### `MethodCall(self, parent, method, n, cycle=None, args=(), kwargs={})`

Class to represent an object's method call that,
when called, schedules itself in the future 

#### Methods

##### `__call__(self, *args, **kwargs)`

Proxy for parent object __call__, calls the enclosed method
and schedules it in the future. 

##### `count(self)`

Counts the number of times this method would have been called between clock start and now 

##### `isScheduled(self)`

Returns True if this is in the Tempo Clock 

##### `update(self, n, cycle, args=(), kwargs={})`

Updates the values of the MethodCall. Re-adjusts
the index if cycle has been changed 

---

### `Repeatable(self)`



#### Methods

##### `after(self, n, cmd, *args, **kwargs)`

Schedule self.cmd(args, kwargs) in 'n' beats time
```
# Stop the player looping after 16 beats
p1 >> pads().after(16, "stop")
```

##### `every(self, n, cmd, *args, **kwargs)`

Every n beats, call a method (defined as a string) on the
object and use the args and kwargs. To call the method
every n-th beat of a timeframe, use the `cycle` keyword argument
to specify that timeframe.

```
# Call the shuffle method every 4 beats

p1.every(4, 'shuffle')

# Call the stutter method on the 5th beat of every 8 beat cycle

p1.every(5, 'stutter', 4, cycle=8)

```

---

## Functions

## Data

