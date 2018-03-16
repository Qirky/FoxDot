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

### `_whenLibrary(self)`

Used to store 'when statements'. Is accessed through the `__when__` object.
    

#### Methods

---

### `_whenStatement(self, func=<lambda>)`



#### Methods

##### `set_namespace(cls, ns)`

Define the namespace to execute the actions. Should be a `dict` 

---

## Functions

## Data

#### `when = {}`

