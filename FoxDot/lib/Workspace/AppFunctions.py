#!/usr/bin/python
""" Collection of functions used in the Workspace package """

from __future__ import absolute_import, division, print_function
from .Format import *
import sys

def stdout(*args):
    """ Forces prints to stdout and not console """
    sys.__stdout__.write(" ".join([str(s) for s in args]) + "\n")

def index(index1, index2=None):
    if type(index1) == str and index2 == None:
        return tuple(int(n) for n in index1.split('.'))
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
    if len(s) == 0:
        return 0
    for i, char in enumerate(s):
        if char != " ":
            break
    return i

def at_function(index, string):
    """ Returns true if the index is at a colon in the string """
    return False if index == 0 else string[index-1] == ":"

def in_brackets(index, string):
    """ Returns true if index is between a pair of brackets (could be non closing) """
    
    left_b = list("({[")
    right_b = list(")}]")

    count = dict([(l,0) for l in left_b])

    index = index - 1 # Look to the character to the left to start

    while index > 0:

        char = string[index]

        if char in left_b:

            if count[char] == 0:

                return True

            else:

                count[char] -= 1

        elif char in right_b:

            count[brackets[char]] += 1

        index -= 1

    return False

def get_tabspace(s):
    """ Returns the amount of whitespace at the start of a string """
    return indented(s) * " "

def open_bracket(text):
    """ Returns the index of the last open bracket """

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
