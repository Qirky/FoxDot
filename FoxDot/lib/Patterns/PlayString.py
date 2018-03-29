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
    def index(self, sub, start=0):
        """ Returns the index of the closing bracket """
        br = "([{<"[")]}>".index(sub)]
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
        err = "Closing bracket {!r} missing in string {!r}".format(sub, "".join(self.original))
        raise ParseError(err)
    
    def next_char_index(self, char, start=0):
        try:
            return self.string[start:].index(char) + start
        except IndexError:
            raise ParseError("No {!r} character found in string {!r}".format(char, self.original))