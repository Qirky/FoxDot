"""
    Patterns.Parse.py
    =================

    Handles the parsing of Sample Player Object Strings
"""

from __future__ import absolute_import, division, print_function

import re

from .PlayString import *

from ..Utils import modi, LCM

class Parser:
    re_nests  = r"\((.*?)\)"
    re_square = r"\[.*?\]"
    re_curly  = r"\{.*?\}"

    def __init__(self):
        self.nested_type=lambda *args: None
        self.square_type=lambda *args: None
        self.braces_type=lambda *args: None

    def __call__(self, string):
        output, _ = self.parse(string)
        return output

    def set_data_types(self, square=None, nested=None, braces=None):
        self.square_type = square if square is not None else self.square_type
        self.nested_type = nested if nested is not None else self.nested_type
        self.braces_type = braces if braces is not None else self.braces_type
        return

    @staticmethod
    def expand(nested_list):
        # Expand any '[]' or '{}' groups
        output = PlayString([])
        for item in nested_list:
            if isinstance(item, PlayString):
                output.extend(item)
            else:
                output.append(item)
        return output

    def parse(self, string):
        # Iterate over the string
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

                chars, _ = self.parse(s)

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

                chars, _ = self.parse(s)

                if len(chars) == 0:

                    e = "Empty '{}' brackets in string"

                    raise(ParseError(e))

                items.append( self.braces_type(chars) )
                    
            # Look for a '[]'
            elif char == "[":
                
                j = string.index("]", start=i+1)
                s = string[i+1:j]
                i = j

                chars, contains_nest = self.parse(s)

                if len(chars) == 0:

                    e = "Empty '[]' brackets in string"

                    raise(ParseError(e))

                # Un-nest
                if contains_nest:

                    # May contain sub-nests, so re-parse with calculated duration

                    chars, _ = self.parse(s)

                    new_chars = []

                    for num in range(max([len(ch) for ch in chars])):

                        new_chars.append(self.square_type([modi(ch, num) for ch in chars]))

                    items.append( new_chars )

                else:

                    new_chars = []

                    for char in chars:

                        new_chars.append(char)

                    items.append( self.square_type(new_chars) )

            # Add single character to list

            elif char not in ")]":

                items.append( char )

            # Increase iterator
            i += 1

        return items, contains_nest

ParsePlayString = Parser()
