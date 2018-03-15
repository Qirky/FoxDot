# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import re
from os.path import abspath, join, dirname

from ..Code import classes, functions, instances
from ..Settings import *

def path(fn):
    return abspath(join(dirname(__file__), fn))

# RegEx Group 1
user_defn = r"(?<=def )(\w+)"
players   = r"(?<=>>)(\s*\w+)"
comments  = r"^\s*#.*|[^\"']*(#[^\"']*$)"
decorator = r"\A\s*@.+"
#numbers   = r"(?<![a-zA-Z])\d+"
numbers   = r"\W+(\d+)"
strings   = r"\".*?\"|\".*" + "|\'.*?\'|\'.*"
dollar    = r"\s\$\s?"
arrow     = r"\s>>\s?"
multiline = r"\"\"\".*\"\"\"|'''.*'''"


# RegEx Group 2
def re_list(string, br="[]"):
    new = ""
    nested = False
    n, m = 0, 0
    while n < len(string):
        char = string[n]
        if char == br[0]:
            if nested is False:
                nested = True
                m = n
                n += 1
            else:
                sub = string[n + 1:string.rfind(br[1])]
                value = re_list(sub)
                n += len(value) + 1
        elif char == br[1]:
            new_string = string[m:n+1]
            return new_string
        else:
            n += 1

def re_pat(string):
    r = r"P?" + re_list(string)
    for char in "[]()":
        r = r.replace(char,"\\" + char)
    return re.search(r, string)

def findstyles(line, *args):
    """ Finds any locations of any regex and returns the name
        of the style and the start and end point in the line """

    if not args:

        tags = re_patterns

    else:

        tags = [a for a in args if a in re_patterns]

    pos = []

    for tag in tags:

        match_start = match_end = 0

        for match in re.finditer(re_patterns[tag], line):

            looking = True

            i = 0

            while looking:

                try:

                    start  = match.start(i)
                    end    = match.end(i)

                    if start == end == -1:

                        raise IndexError # this is hacky af

                    match_start = start
                    match_end   = end

                except IndexError:

                    looking = False

                i += 1

            pos.append((tag, match_start, match_end))

    return pos

def userdefined(line):
    """ Returns the name of a user defined function or class in a string
        i.e. def foo(x) -> foo """

    match = re.search(user_defn, line)

    if match:

        return match.group()

def find_comment(line):
    """ Finds the index of a comment # and returns None if not found """
    instring, instring_char = False, ""
    for i, char in enumerate(line):
        if char in ('"', "'"):
            if instring:
                if char == instring_char:
                    instring = False
                    instring_char = ""
            else:
                instring = True
                instring_char = char
        elif char == "#":
          if not instring:
              return i
    return None

def find_multiline(text):
    pos = []

    tag = multiline

    match_start = match_end = 0

    for match in re.finditer(tag, text, re.DOTALL):

        looking = True

        i = 0

        while looking:

            try:

                start  = match.start(i)
                end    = match.end(i)

                if start == end == -1:

                    raise IndexError # this is hacky af

                match_start = start
                match_end   = end

            except IndexError:

                looking = False

            i += 1

        pos.append((match_start, match_end))

    return pos


# Use our regex to read patterns.py and add all the functions to key_types
    
from ..Patterns import Main, Sequences, Generators
from ..SCLang import SCLang

foxdot_kw = ["Clock","Group","Scale","DefaultServer","Root","Samples","var","Pvar",
             "linvar","expvar","mapvar","sinvar","inf","when", "lambda", u"λ", decorator]

foxdot_funcs = classes(Main) + classes(Generators) + functions(Sequences) + ["P"]

# Python keywords used in RegEx Group 2

py_indent_kw = ["for","if","elif","else","def","while","class","try","except"]

py_functions = ["if","elif","else","return","def","print","when","from",
                 "and","or","not","is","in","for","as","with", "global",
                 "while", "class", "import", "try","except","from","break"]

py_other_kws = foxdot_kw + ["True", "False", "None", "self"]

py_key_types = ["abs","divmod","input","open","staticmethod","all","enumerate","int",
                "ord","str","any","eval","isinstance", "pow","sum","basestring",
                "execfile","issubclass","super","bin","file","iter","property","tuple",
                "bool", "filter","len","range","type","bytearray","float","list",
                "raw_input","unichr","callable","format","locals","reduce","unicode",
                "chr","frozenset","long","reload","vars","classmethod","getattr","map",
                "repr","xrange","cmp","globals","max","reversed","zip","compile","hasattr",
                "memoryview","round","__import__","complex","hash","min","delattr","set",
                "help","next","setattr","dict","hex","object","slice","dir","id","sorted"]

py_key_types = foxdot_funcs + py_key_types

py_separators = list("[](){},./*+=- \t\n")
py_whitespace = list(" \t\n\r\f\v")

left_b = list("([{'\"")
right_b = list(")]}'\"")
brackets = dict([(right_b[i],left_b[i]) for i in range(3)])
tabsize = 4

# RegEx Group 2

functions = r"(?<![a-zA-Z._])(" + "|".join(py_functions) + ")(?![_a-zA-Z])"
key_types = r"(?<![a-zA-Z._])(" + "|".join(py_key_types) + ")(?![_a-zA-Z])"
#key_types = r"\.?(\w+)\(|\W+P\W+" # TODO - change py_key_types to just and value followed by ()?
other_kws = r"(?<![a-zA-Z._])(" + "|".join(py_other_kws) + ")(?![_a-zA-Z])"

colour_map = {'plaintext'  : COLOURS.plaintext,
              'background' : COLOURS.background,
              'functions'  : COLOURS.functions,
              'key_types'  : COLOURS.key_types,
              'user_defn'  : COLOURS.user_defn,
              'other_kws'  : COLOURS.other_kws,
              'comments'   : COLOURS.comments,
              'numbers'    : COLOURS.numbers,
              'strings'    : COLOURS.strings,
              'dollar'     : COLOURS.dollar,
              'arrow'      : COLOURS.arrow,
              'players'    : COLOURS.players}

re_patterns = {  'functions' : functions,
                 'key_types' : key_types,
                 'user_defn' : user_defn,
                 'other_kws' : other_kws,
                 'numbers'   : numbers,
                 'strings'   : strings,
                 'dollar'    : dollar,
                 'arrow'     : arrow,
                 'players'   : players }


bracket_formatting = {'borderwidth': 2,
                      'relief' : 'groove'}

# Weightings (heavier get checked last)

tag_weights = [['numbers'],
               ['key_types','functions','user_defn','other_kws','dollar','arrow','players'],
               ['strings'],
               ['comments']]

def get_keywords():
    return list(set(py_indent_kw + py_functions + py_other_kws + py_key_types))
