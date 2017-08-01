"""
    Patterns.Parse.py
    =================

    Handles the parsing of Sample Player Object Strings
"""

from __future__ import absolute_import, division, print_function

import re

from .PlayString import *
from .Generators import PRand
from .PGroups    import PGroupStar
from .Main       import metaPattern, PatternMethod

from ..Utils import modi, LCM

re_nests  = r"\((.*?)\)"
re_square = r"\[.*?\]"
re_curly  = r"\{.*?\}"
square_type=PGroupStar
braces_type=PRand

def ParsePlayString(string):
    output, _ = feed(string)
    return output

def feed(string):
    string = PlayString(string)
    items = []
    contains_nest = False
    i = 0
    while i < len(string):
        char = string[i]

        # Look for a '()'
        if char == "(":

            # Parse the contents of the brackets if found
            j = string.index(")", start=i+1)
            
            s = string[i+1:j]
            i = j

            chars, _ = feed(s)

            if len(chars) == 0:

                e = "Empty '()' brackets in string"

                raise(ParseError(e))

            items.append( chars )

            contains_nest = True

        # Look for a '{}'
        elif char == "{":

            # Parse the contents of the brackets if found
            j = string.index("}", start=i+1)
            s = string[i+1:j]
            i = j

            chars, _ = feed(s)

            if len(chars) == 0:

                e = "Empty '{}' brackets in string"

                raise(ParseError(e))

            items.append( braces_type(chars) )
                
        # Look for a '[]'
        elif char == "[":
            
            j = string.index("]", start=i+1)
            s = string[i+1:j]
            i = j

            chars, contains_nest = feed(s)

            if len(chars) == 0:

                e = "Empty '[]' brackets in string"

                raise(ParseError(e))

            # Un-nest
            if contains_nest:

                # May contain sub-nests, so re-parse with calculated duration

                chars, _ = feed(s)

                new_chars = []

                for num in range(max([len(ch) for ch in chars])):

                    new_chars.append(square_type([modi(ch, num) for ch in chars]))

                items.append( new_chars )

            else:

                new_chars = []

                for char in chars:

                    new_chars.append(char)

                items.append( square_type(new_chars) )

        # Add single character to list

        elif char not in ")]":

            items.append( char )

        # Increase iterator
        i += 1

    return items, contains_nest

@PatternMethod
def fromString(self, string):
    self.data = ParsePlayString(string)
    self.make()
    return self
