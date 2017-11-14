"""
    Patterns.Parse.py
    =================

    Handles the parsing of Sample Player Object Strings
"""

from __future__ import absolute_import, division, print_function

import re

from .PlayString import *
from .Generators import PRand
from .PGroups    import PGroupMod
from .Main       import Pattern, metaPattern, PatternMethod

from ..Utils import modi, LCM

re_nests  = r"\((.*?)\)"
re_square = r"\[.*?\]"
re_curly  = r"\{.*?\}"
re_arrow  = r"<.*?>"
square_type=PGroupMod
braces_type=PRand

def ParsePlayString(string):
    output, _ = feed(string)
    return output

def feed(string):
    
    string = PlayString(string)
    items  = Pattern() # The actual pattern

    layer_pattern = False
    contains_nest = False
    
    i = 0
    
    while i < len(string):

        char = string[i]

        # look for a '<>'
        if char == "<":

            # Parse the contents of the brackets if found
            j = string.index(">", start=i+1)
            s = string[i+1:j]
            i = j

            chars, _ = feed(s)

            if len(chars) == 0:

                e = "Empty '<>' brackets in string"

                raise ParseError(e)

            if layer_pattern:

                items.data[-1] = (items.data[-1] & chars)

            else:

                items.data.append(chars)

                layer_pattern = True

            contains_nest = True

        # Look for a '()'
        elif char == "(":

            # Parse the contents of the brackets if found
            j = string.index(")", start=i+1)
            
            s = string[i+1:j]
            i = j

            chars, _ = feed(s)

            if len(chars) == 0:

                e = "Empty '()' brackets in string"

                raise ParseError(e)

            items.data.append( chars )

            layer_pattern = False

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

                raise ParseError(e)

            items.data.append( braces_type(chars) )

            layer_pattern = False
                
        # Look for a '[]'
        elif char == "[":
            
            j = string.index("]", start=i+1)
            s = string[i+1:j]
            i = j

            chars, contains_nest = feed(s)

            if len(chars) == 0:

                e = "Empty '[]' brackets in string"

                raise ParseError(e)

            # Un-nest
            if contains_nest:

                # May contain sub-nests, so re-parse with calculated duration

                # chars, _ = feed(s) # why do this again?

                new_chars = []

                largest_item = max([len(ch) for ch in chars.data])

                for num in range(largest_item):

                    new_chars.append(square_type([modi(ch, num) for ch in chars.data]))

                items.data.append( new_chars )

                layer_pattern = False

            else:

                new_chars = []

                for char in chars:

                    new_chars.append(char)

                items.data.append( square_type(new_chars) )

                layer_pattern = False

        # Add single character to list

        elif char not in ")]}>":

            items.data.append( char )

            layer_pattern = False

        # Increase iterator
        i += 1

    return items, contains_nest


@PatternMethod
def fromString(self, string):
    self.data = ParsePlayString(string).data
    return self
