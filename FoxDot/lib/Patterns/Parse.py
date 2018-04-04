"""
    Patterns.Parse.py
    =================

    Handles the parsing of Sample Player Object Strings
"""

from __future__ import absolute_import, division, print_function

import re

from .PlayString import *
from .Generators import PRand
from .PGroups    import PGroupMod, PGroupOr, PGroupStar, PGroupPlus
from .Main       import Pattern, metaPattern, PatternMethod, PGroup, GeneratorPattern

from ..Utils import modi, LCM

re_nests  = r"\((.*?)\)"
re_square = r"\[.*?\]"
re_curly  = r"\{.*?\}"
re_arrow  = r"<.*?>"
square_type = PGroupPlus
braces_type = PRand
bar_type    = PGroupOr

def ParsePlayString(string, flat=False):
    """ Returns the parsed play string used by sample player """
    output, _ = feed(string)
    return output

def convert_to_int(data):
    """ Recursively calls until all nested data contains only integers """
    if isinstance(data, (int, float, str)):
        return int(data)
    elif isinstance(data, (list, tuple)):
        return data.__class__([convert_to_int(item) for item in data])
    elif isinstance(data, GeneratorPattern):
        return data.transform(convert_to_int)
    elif isinstance(data, metaPattern):
        return data.convert_data(convert_to_int)
    return int(data)

def arrow_zip(pat1, pat2):
    """ Zips two patterns together. If one item is a tuple, it extends the tuple / PGroup
        i.e. arrow_zip([(0,1),3], [2]) -> [(0,1,2),(3,2)]
    """
    output = Pattern()

    for i in range(LCM(len(pat1), len(pat2))):

        item1 = pat1.getitem(i, get_generator=True)
        item2 = pat2.getitem(i, get_generator=True)

        if all([x.__class__== PGroup for x in (item1, item2)]):

            new_item = PGroup(item1.data + item2.data)

        elif item1.__class__ == PGroup:

            new_item = PGroup(item1.data + [item2])

        elif item2.__class__ == PGroup:

            new_item = PGroup([item1] + item2.data)

        else:

            new_item = (item1, item2)

        output.append(new_item)

    return output

def feed(string):
    """ Used to recursively parse nested strings, returns a list object (not Pattern),
        and a boolean denoting if the list contains a nested list """
    
    string = PlayString(string)
    items  = [] # The actual pattern

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

            # If we know we are layering, zip the last item

            if layer_pattern:

                items[-1] = items[-1].zip( Pattern(chars) )

            else:

                items.append(Pattern(chars))

                layer_pattern = True

            contains_nest = True

        # Look for || for specifying sample numbers

        elif char == "|":

            # Parse the contents of the brackets if found
            j = string.next_char_index("|", start=i+1)
            s = string[i+1:j]
            i = j

            chars, _ = feed(s)

            if len(chars) == 0:

                e = "Empty '||' delimeters in string"

                raise ParseError(e)

            try:

                assert(len(chars) == 2)

            except AssertionError:

                e = "'||' delimeters must contain exactly 2 elements"

                raise ParseError(e)

            # First is our list of sample chars
            
            samp_chr = chars[0]

            # Next is a list of integers for sample kw

            samp_num = convert_to_int(chars[1])

            # print(samp_chr, samp_num)

            items.append(bar_type((samp_chr, samp_num)))

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

            items.append( chars ) # add the nested list

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

            items.append( braces_type(chars) )

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

                new_chars = []

                largest_item = max([len(ch) for ch in chars])

                for num in range(largest_item):

                    new_chars.append(square_type([modi(ch, num) for ch in chars]))

                items.append( new_chars )

                layer_pattern = False

            else:

                new_chars = []

                for char in chars:

                    new_chars.append(char)

                items.append( square_type(new_chars) )

                layer_pattern = False

        # Add single character to list

        elif char not in ")]}>|":

            items.append( char )

            layer_pattern = False

        # Increase iterator
        i += 1

    return items, contains_nest


@PatternMethod
def fromString(self, string):
    self.data = ParsePlayString(string)
    self.make()
    return self
