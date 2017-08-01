from __future__ import absolute_import, division, print_function

import re
from random import shuffle, choice

re_nests  = r"\((.*?)\)"
re_square = r"\[.*?\]"
re_curly  = r"\{.*?\}"
re_chars  = r"[^[\](){}]"
br_pairs = {"(":")",
            ")":"(",
            "[":"]",
            "]":"[",
            "{":"}",
            "}":"{"}

class ParseError(Exception):
    pass

class PlayString:
    """ Container for character objects """
    contains_nest = False
    def __init__(self, string):
        self.string   = list(string)
        self.original = str(string)
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
    def multiply(self, value):
        for char in self.string:
            char.multiply(value)
        return
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
        raise ParseError("Closing bracket '%s' missing in string '%s'" % (sub, self.original))

    # Return strings
    
    def shuffle(self):
        """ Proper method of shuffling playstrings as opposed to shuffle() """

        # 1. Get all the characters out in order

        chars = re.findall(re_chars, self.original)

        string = re.sub(re_chars, "%s", self.original)

        # 2. Shuffle

        shuffle(chars)

        # 3. replace

        return string % tuple(chars)

    def mirror(self):
        l = list(self.original)
        l.reverse()
        for i, char in enumerate(l):
            if char in br_pairs.keys():
                l[i] = br_pairs[char]
        return "".join(l)

    def rotate(self, n=1):
        # 1. Get all the characters out in order

        chars = re.findall(re_chars, self.original)

        string = re.sub(re_chars, "%s", self.original)

        # 2. Rotate
    
        n = int(n)

        chars = chars[n:] + chars[:n]

        return string % tuple(chars)


