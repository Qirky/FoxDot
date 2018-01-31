Getting Started
===============

Also available in `Spanish`_.

Python is an object-oriented programming language that focusses on flexibility and readability. It also contains a large library of functions and serves a large user base. So it’s about time we were about to live code music with it.

If you’re ever stuck, or want to know more about a function or class – just type ``help`` followed by the name of that Python object in brackets: ::

    help(object)

FoxDot provides a Python interface to SuperCollider – mainly as a quick and easy to use abstraction for SuperCollider classes, `Pbind`_ and `SynthDef`_. Please read the SuperCollider documentation if you’d like to know more.

A SynthDef is essentially your digital instrument and FoxDot creates players that use these instruments with your guidance. To execute code in FoxDot, make sure your text cursor is in the ‘block’ of code (sections of text not separated by blank lines) and press ``Ctrl+Return``. The output of any executed code is displayed in the console in the bottom half of the window.

*Try* ``print(2+2)`` *and see what you get.*

*Now try something that spans multiple lines:* ::

    for n in range(10):
        sq = n*n
        print(n, sq)

1. Player Objects
-----------------

It is, in fact, possible to create SuperCollider SynthDefs using FoxDot, but that’s outside of the scope of this starter guide. To have a look at the existing (but quite small, unfortunately) library of FoxDot SynthDefs, just execute: ::

    print(SynthDefs)

Choose one and create a FoxDot player object using the double arrow syntax like in the example below. If my chosen SynthDef was “pluck” then I could create an object “p1”: ::

    p1 >> pluck()

To stop an individual player object, simply execute ``p1.stop()``. To stop all player objects, you can press ``Ctrl+.``, which is a shortcut for the command ``Clock.clear()``.

The ``>>`` in Python is usually reserved for a type of operation, like + or -, but it is not the case in FoxDot, and the reason will become clear shortly. If you now give your player object some arguments, you can change the notes being played back. The first argument, the note degree, doesn’t need explicit naming, but you’ll need to specify whatever else you want to change – such as note durations or amplitudes. ::

    p1 >> pluck([0,2,4], dur=[1,1/2,1/2], amp=[1,3/4,3/4])

These keyword arguments relate to the corresponding SynthDef (“pluck” in this case) but with a few exceptions:

* degree
* dur
* scale
* oct

These are used by FoxDot to calculate the frequencies of notes to be played and when to play them. You can view the SuperCollider code (although not easy to read) by executing ``print(pluck)`` for example. You can group together sounds by putting multiple values within an argument in round brackets like so: ::

    b1 >> bass([(0,9),(3,7)], dur=4, pan=(-1,1))

Notice how you don’t need to put single values in square brackets? FoxDot takes care of that for you. You can even have a Player Object follow another! ::

    b1 >> bass([0,2,3,4], dur=4)
    p1 >> pluck(dur=1/2).follow(b) + (0,2,4) # This adds a triad to the bass notes

Sound samples can also be played back using the Sample Player object, which is created like so: ::

    d1 >> play("x-o-")

Each character refers to a different audio file. To play samples simultaneously, simply create a new player object: ::

    d1 >> play("xxox")
    hh >> play("---(-=)", pan=0.5)

Characters in round brackets are alternated in each loop (know as lacing) such that the above player, ``hh``, would be writtern literally as ``hh >> play('-------=')`` which save you a lot of typing! Putting characters in square brackets will play them twice as fast and can be put in round brackets as if they were one character themselves. Try it out: ::

    d1 >> play("x[--]o(=[-o])")

2. Patterns
-----------
Player Objects use Python lists, known more commonly as arrays in other languages, to sequence themselves. You’ve already used these previously, but they aren’t exactly flexible for manipulation. For example, try multiplying a list by two like so: ::

    print([1, 2, 3] * 2)

Is the result what you expected? If you want to manipulate the internal values in Python you have to use a for loop: ::

    l = []
    for i in [1, 2, 3]:
        l.append(i * 2)
    print(l)

or list comprehension: ::

    print([i*2 for i in [1,2,3]])

But what if you want to multiply the values in a list by 2 and 3 in an alternating way? That requires quite a lot of messing around actually, especially if you don’t know what values you’ll be using. FoxDot uses a container type called a ‘Pattern’ to help solve this problem. They act like regular lists but any mathematical operation performed on it is done to each item in the list and done so pair-wise if using a second pattern. The base Pattern can be created like so: ::

    print(P[1,2,3] * 2)
    >>> P[2, 4, 6]
    print(P[1,2,3] + [3,4])
    >>> P[4, 6, 6, 5, 5, 7]

Notice how in the second operation, the output consists of all the combinations of the two patterns i.e. ``[1+3, 2+4, 3+3, 1+4, 2+3, 3+4]``.

* Try some other mathematical operators and see what results you get.
* What happens when you group numbers in brackets, like P[1,2,3] * (1,2)?

There are several other Pattern classes in FoxDot that help you generate arrays of numbers but also behave in the same way as the base Pattern. We’ll just look at two types here, but execute ``print(classes(Patterns.Sequences))`` to see what others exist and have a go at using them.

In Python, you can generate a range of integers with the syntax ``range(start, stop, step``). By default, start is 0 and step is 1. You can use ``PRange(start, stop, step)`` to create a Pattern object with the equivalent values: ::

    print(range(10))
    >>> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(PRange(10))
    >>> P[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(PRange(10) * [1, 2])           # Pattern class behaviour
    >>> P[0, 2, 2, 6, 4, 10, 6, 14, 8, 18]

But what about combining patterns? In Python, you can concatenate two lists (append one to another) by using the ``+`` operator but FoxDot Patterns use this to perform addition to the data within the list. To connect two Pattern objects together, you can use the pipe symbol, ``|``, which Linux users might be familiar with – it is used to connect command line programs by sending output from one process as input to another. ::

    print(PRange(4) | [1,7,6])
    >>> P[0, 1, 2, 3, 1, 7, 6]

FoxDot automatically converts any object being piped to a Pattern to the base Pattern class so you don’t have to worry about making sure everything is the right type. There exists several types of Pattern sequences in FoxDot (and the list is still growing) that make generating these numbers a little easier. For example, to play the first octave of a pentatonic scale from bottom to top and back again, you might use two ``PRange`` objects: ::

    p1 >> pluck(PRange(5) | PRange(5,0,-1), scale=Scale.default.pentatonic)

The ``PTri`` class does this for you: ::

    p1 >> pluck(PTri(5), scale=Scale.default.pentatonic)

3. TimeVars
-----------
A ``TimeVar`` is an abbreviation of “Time Dependent Variable” and is a key feature of FoxDot. A TimeVar has a series of values that it changes between after a pre-defined number of beats and is created using a ``var`` object with the syntax ``var([list_of_values],[list_of_durations])``. Example: ::

    a = var([0,3],4)            # Duration can be single value
    print(int(Clock.now()), a)   # 'a' initally has a value of 0
    >>> 0, 0
    print(int(Clock.now()), a)   # After 4 beats, the value changes to 3
    >>> 4, 3
    print(int(Clock.now()), a)   # After another 4 beats, the value changes to 0
    >>> 8, 0

When a TimeVar is used in a mathematical operation, the values it affects also become TimeVars that change state when the original TimeVar changes state – this can even be used with patterns: ::

    a = var([0,3], 4)
    print(a + 5)        # beat = 0
    >>> 5
    print(a + 5)        # beat = 4
    >>> 8
    b = PRange(4) + a
    print(b)             # beat = 8 and a has a value of 0
    >>> P[0, 1, 2, 3]
    print(b)             # beat = 12 and a has a value of 3
    >>> P[3, 4, 5, 6]

.. _Spanish: https://github.com/rubentr/FoxDot-Starter-Guide-ES/
.. _Pbind: http://doc.sccode.org/Tutorials/A-Practical-Guide/PG_03_What_Is_Pbind.html
.. _SynthDef: http://doc.sccode.org/Classes/SynthDef.html

