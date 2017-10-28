"""

A `Pattern` object is a container-like object, similar to Python lists, but with slightly different behaviour.
The two most notable differences are how they behave when used with arithmetic operators and
how they behave when indexed. A `Pattern` can be created by instantiating the class like so:

    myPattern = Pattern([0,1,2,3])

This returns an a `Pattern` with the contents `[0,1,2,3]`. This is simply written as `P[0,1,2,3]`.
You can also use this shorthand to create a pattern:

    myPattern = P[0,1,2,3]

When using this method of instantiating a `Pattern` you can use Python slices to generate a 
range of numbers. The following creates the pattern `P[0,1,2,3,4,6,8,10]`:

    myPattern = P[0:4,4:12:2]

Nested lists in a `Pattern` are treated not as single elements but as alternating values
when indexing the `Pattern` with values greater than the apparent length of the  `Pattern`.
The following two `Pattern` objects are identical:

    >>> a = P[0,1,2,[3,4]]
    >>> b = P[0,1,2,3,0,1,2,4]
    >>> a[3], b[3]
    3, 3
    >>> a[7], b[7]
    4, 4
    >>> a == b
    True

No matter what the index, the `Pattern` will return a value, usually `pat[i % len(pat)]` where
`i` is the index and `pat` is a `Pattern`. Nested values are accessed in turn depending
on how large the index is.

Nested `tuples` become instances of the `PGroup` class when used in a `Pattern`, which
are containers with similar behaviour to the `Pattern` class but are not accessed alternatively
when nested, but all values are returned. You can instantiate a `PGroup` in similar manner
to instantiating a `Pattern`

    myGroup1 = PGroup([0,1,2])
    myGroup2 = P(0,1,2)

If I try and instantiate a `PGroup` with a `list` or `Pattern` as an element then a `Pattern`
of `PGroups` is returned instead, alternating the values in the slot that was a list:

    >>> P(0,1,[2,3,4])
    P[P(0, 1, 2), P(0, 1, 3), P(0, 1, 4)]

Similar to `numpy` arrays, arithmetic operations are performed on all elements of a `Pattern`,
including nested `Patterns` and `PGroups`. If I use a `list` or `Pattern` of values in an operation 
(we will use  addition as an example) then each value is added in sequence until all values are added
together:

    # Basic addition
    >>> P[0, 1, [2, 3], 4, (5,6)] + 2
    P[2, 3, P[4, 5], 6, P(7, 8)]

    # Using a Pattern of values
    >>> P[0, 1, [2, 3], 4, (5,6)] + P[2, 4]
    P[2, 5, P[4, 5], 8, P(7, 8), 4, 3, P[6, 7], 6, P(9, 10)]

`Patterns` also have many useful methods for manipulating the order of values, such as `palindrome`
or `rotate`, and can be "chained" together as these don't affect the order in place and return
the augmented version of the `Pattern`.


"""

from __future__ import absolute_import, division, print_function

from .Main       import *
from .Operations import *
from .Sequences  import *
from .PGroups    import *
from .Generators import *
from .PlayString import *
from .Parse      import *
from .Utils      import *
