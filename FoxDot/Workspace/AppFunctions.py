#!/usr/bin/python
""" Collection of functions used in the App package """

from Format import *

def index(index1, index2=None):
    if type(index1) == str and index2 == None:
        return [int(n) for n in index1.split('.')]
    return str(index1) + '.' + str(index2)

def empty(string):
    return len(string.replace(' ','')) == 0

def isDelete(char):
    return char == "\x08"

def isReturn(char):
    return char == "\r"

def isHex(char):
    return len(repr(char)) > 3

def indented(s):
    for i, char in enumerate(s):
        if char != " ":
            break
    return i

def open_bracket(text):

    count = dict([(l,0) for l in left_b])

    for i, char in enumerate(text):

        if   char in left_b:

            count[char] += 1

        elif char in right_b:

            count[brackets[char]] -= 1

    open_br = [b for b in count.keys() if (count[b] >= max(count.values()) > 0) and (count[b] % 2 == 1) ]

    pos = [text.rfind( b ) for b in open_br]

    if pos:

        return max(pos) + 1

def function(text):

    tokens = text.strip()

    if tokens[-1] != ":":

        return

    tokens = tokens[:-1]
    
    for b in left_b + right_b:
        
        tokens = tokens.replace(b," ")

    tokens = tokens.split()

    for kw in py_indent_kw:

        if kw in tokens:

            return indented(text) + tabsize
