"""
    Patterns.Parse.py
    =================

    Handles the parsing of Sample Player Object Strings
"""

import re
import Main
from utils import modi, LCM
from PlayString import *


class Parser:
    re_nests  = r"\((.*?)\)"
    re_square = r"\[.*?\]"
    re_curly  = r"\{.*?\}"

    def __call__(self, string):
        output, _ = self.parse(string)
        return output

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

    def parse(self, string, dur=1):
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

                chars, _ = self.parse(s, dur)

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

                chars, _ = self.parse(s, dur)

                if len(chars) == 0:

                    e = "Empty '{}' brackets in string"

                    raise(ParseError(e))

                items.append( Main.PRand(chars) )
                    
            # Look for a '[]'
            elif char == "[":
                
                j = string.index("]", start=i+1)
                s = string[i+1:j]
                i = j

                chars, contains_nest = self.parse(s, dur)

                if len(chars) == 0:

                    e = "Empty '[]' brackets in string"

                    raise(ParseError(e))

                # Un-nest
                if contains_nest:

                    # May contain sub-nests, so re-parse with calculated duration

                    chars, _ = self.parse(s, dur / float(len(chars)))

                    new_chars = []

                    for num in range(max([len(ch) for ch in chars])):

                        # new_chars.append(PlayGroup([modi(ch, num) for ch in chars]))
                        new_chars.append(Main.PGroupStar([modi(ch, num) for ch in chars]))

                    items.append( new_chars )

                else:

                    new_chars = []

                    for char in chars:

                        # char.divide(len(chars))

                        #if isinstance(char, PCHAR): 
                        #if isinstance(char, PlayGroup):
##                        if isinstance(char, Main.PGroupStar):
##
##                            new_chars.extend(char)
##
##                        else:

##                            new_chars.append(char)

                        new_chars.append(char)

                    # items.append( PlayGroup(new_chars) )
                    items.append( Main.PGroupStar(new_chars) )

            # Add single character to list

            elif char not in ")]":

                items.append( PCHAR(char, dur) )

            # Increase iterator
            i += 1

        return items, contains_nest

Parse = Parser()
