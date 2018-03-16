# `foxdot_when_statement`

How to use `when` statements
----------------------------

A `when` statement is similar to your traditional `if` statement but
instead of evaluating the expression at the time the code is run, it
is constantly testing it to see if it is true.abs

Example 1
---------
::

    when 5 < 10:
        print True
    else:
        print False

Currently there is no `elif` statement implemented yet and lines of code
cannot be spread over multiple lines.

To "stop" an individual `when` statement from monitoring its test. You
need to call the `__when__` object with a `lambda` expression equalling
that of the test and call the `remove` method.

Example 2
---------
::

    a, b = 5, 10

    when a > b:
        print "a is bigger"
    else:
        print "b is bigger"

    # This is how to 'stop' the statement above

    __when__(lambda: a > b).remove()

    # This removes *all* currently running when statements

    __when__.reset()

## Classes

### `_whenStatement(self, func=<lambda>)`



#### Methods

##### `__init__(self, func=<lambda>)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

##### `elsedo(self, func)`

Set the instructions for when the test expression is False. Should
be a list of strings. 

##### `evaluate(self)`

Calls the test expression, and if it has changed then
run the appropriate response code 

##### `reset(self)`

Sets the `when` and `else` actions to nothing 

##### `set_namespace(cls, ns)`

Define the namespace to execute the actions. Should be a `dict` 

##### `then(self, func)`

Set the instructions for when the test expression is True. Should
be a list of strings. 

##### `toggle_live_functions(self, switch)`

If the action functions are @livefunctions, turn them on/off 

---

### `_whenLibrary(self)`

Used to store 'when statements'. Is accessed through the `__when__` object.
    

#### Methods

##### `__call__(self, name, **kwargs)`

Calling when() with no arguments will evaluate all expressions
stored in self.library. Calling with func as a valid function
will see if the function is in self.library and add it if not,
or update do  / elsedo

##### `__init__(self)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__repr__(self)`

Return repr(self).

##### `reset(self)`

Clears the library and stop scheduling 

##### `run(self)`

Continual loop evaluating when_statements
        

---

## Functions

## Data

#### `when = {}`

