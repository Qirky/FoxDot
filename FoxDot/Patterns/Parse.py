"""
    Patterns.Parse.py
    =================

    Handles the parsing of Sample Player Object Strings
"""

import re
try:
    from Operations import modi, LCM
except:
    def modi(array, i, debug=0):
        """ Returns the modulo index i.e. modi([0,1,2],4) will return 1 """
        try:
            return array[i % len(array)]
        except:        
            return array

    def LCM(*args):
        """ Lowest Common Multiple """
        # Base case
        if len(args) == 1:
            return args[0]
        
        X = list(args)
        
        while any([X[0]!=K for K in X]):

            i = X.index(min(X))
            X[i] += args[i]        

        return X[0]

class PlayString:
    """ Container for PCHAR objects """
    contains_nest = False
    def __init__(self, string):
        self.string = list(string)
    def __repr__(self):
        return repr(self.string)
    def __len__(self):
        return len(self.string)
    def __getitem__(self, key):
        return self.string[key]
    def __setitem__(self, key, value):
        self.string[key] = value
    def get_dur(self):
        """ Returns a list of durations """
        return [char.get_dur() for char in self.string]
    def append(self, item):
        self.string.append(item)
    def extend(self, items):
        self.string.extend(items)
    def index(self, sub, start=0):
        """ Returns the index of the closing bracket """
        br = "([{"[")]}".index(sub)]
        count = 0
        for i in range(start, len(self.string)):
            char = self.string[i]
            if char == br:
                count += 1
            elif char == sub:
                if count > 0:
                    count -= 1
                else:
                    return i
        raise SyntaxError
            

class PCHAR:
    def __init__(self, char, dur=1):
        self.char = char
        self.dur  = dur
    def __len__(self):
        return 1
    def __str__(self):
        return self.char
    def __repr__(self):
        return repr(self.char)
    def get_dur(self):
        return self.dur
        

class Parser:
    re_nests  = r"\((.*?)\)"
    re_square = r"\[.*?\]"
    re_curly  = r"\{.*?\}"

    def __call__(self, string):
        output = self.parse(string)
        while any([len(x) > 1 for x in output]):
            output = self.expand(output)
        return output

    @staticmethod
    def expand(unnested):
        # Expand any '[]' or '{}' groups
        output = PlayString([])
        for item in unnested:
            if len(item) > 1:
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
