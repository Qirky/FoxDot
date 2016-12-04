"""
    Patterns.Parse.py
    =================

    Handles the parsing of Sample Player Object Strings
"""

import re
from Operations import modi, LCM
from PlayString import *

class Parser:
    re_nests  = r"\((.*?)\)"
    re_square = r"\[.*?\]"
    re_curly  = r"\{.*?\}"

    def __call__(self, string):
        output = self.parse(string)
        while any([isinstance(x, PlayString) for x in output]):
            output = self.expand(output)
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
        items = PlayString([])
        index = []
        i = 0
        counter = 0
        while i < len(string):
            char = string[i]
            # Look for a '()'
            if char == "(":
                # Parse the contents of the brackets if found
                j = string.index(")", start=i+1)
                s = string[i+1:j]
                i = j
                items.append(self.parse(s, dur))
                index.append(len(items)-1)
                items.contains_nest = True
                if items[-1].contains_nest:
                    items[-1] = self.expand(items[-1])
            # Look for a '[]'
            elif char == "[":
                j = string.index("]", start=i+1)
                s = string[i+1:j]
                i = j
                items.append(self.parse(s, dur / 2.0))
                if items[-1].contains_nest:
                    index.append(len(items)-1)
                    items.contains_nest = True
            # Look for a '{}'
            elif char == "{":
                j = string.index("}", start=i+1)
                s = string[i+1:j]
                i = j
                chars = self.parse(s, dur)
                # If there is a nest,  re-parse using known length / duration
                if chars.contains_nest:
                    chars = self.parse(s, dur / float(len(chars[0])))
                else:
                    for char in chars:
                        char.dur = char.dur / float(len(chars))
                items.append(chars)
                if items[-1].contains_nest:
                    index.append(len(items)-1)
                    items.contains_nest = True
            # Add single character to list
            elif char not in ")]}":
                items.append( PCHAR(char, dur) )
            # Increase iterator
            i += 1
        # If we have no nests, skip this step
        nests = [len(items[i]) for i in index]
        # After conversion, un-nest the values
        if items.contains_nest == True:
            size = LCM(*nests)
            output = PlayString([PlayString([]) for x in range(size)])
            for n in range(size):
                for i in range(len(items)):
                    char = items[i]
                    # Un-nest if index is stored
                    if i in index:
                        output[n].append(modi(char, n))
                    else:
                        output[n].append(char)
            items = output
            items.contains_nest = True
        return items

Parse = Parser()
