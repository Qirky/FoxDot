import re
from os.path import abspath, join, dirname
from ..Code import classes, functions, instances

def path(fn):
    return abspath(join(dirname(__file__), fn))

# RegEx Group 1
user_defn = r"(?<=def )(\w+)"
players   = r"(?<=>> )(\w+)"
comments  = r"#.*"
numbers   = r"(?<![a-zA-Z])\d+"
strings   = r"\".*?\"|\".*" + "|\'.*?\'|\'.*"
dollar    = r"\s\$\s?"
arrow     = r"\s>>\s?"

def findstyles(line, *args):
    """ Finds any locations of any regex and returns the name
        of the style and the start and end point in the line """

    if not args:

        tags = re_patterns

    else:

        tags = [a for a in args if a in re_patterns]

    pos = []

    for tag in tags:

        for match in re.finditer(re_patterns[tag], line):

            pos.append((tag, match.start(), match.end()))

    return pos

def userdefined(line):
    """ Returns the name of a user defined function or class in a string
        i.e. def foo(x) -> foo """

    match = re.search(user_defn, line)

    if match:

        return match.group()
    

# Use our regex to read patterns.py and add all the functions to key_types
    
from ..Patterns import Sequences, Feeders
from ..SuperCollider import SCLang

foxdot_kw = ["Clock","Group","group","Scale","Server","Root","BufferManager"] + ["var","Pvar","linvar","inf"]

foxdot_funcs = classes(Sequences) #+ functions(Feeders) + instances(SCLang, SCLang.cls) + instances(SCLang, SCLang.EnvGen)

# Python keywords used in RegEx Group 2

py_indent_kw = ["for","if","elif","else","def","while","class","try","except","when"]

py_functions = ["if","elif","else","return","def","print","when","from",
                 "and","or","not","is","in","for","as","with","lambda",
                 "while", "class", "import", "try","except","from"]

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

functions = r"(?<![a-zA-Z.])(" + "|".join(py_functions) + ")(?![a-zA-Z])"
key_types = r"(?<![a-zA-Z.])(" + "|".join(py_key_types) + ")(?![a-zA-Z])"
other_kws = r"(?<![a-zA-Z.])(" + "|".join(py_other_kws) + ")(?![a-zA-Z])"

# Load Default Colour Values

try:

    with open(path("../Settings/text_colour.txt")) as f:

        data = f.readlines()

except:

    data = ["plaintext=#ffffff",
            "background=#4d4d4d",
            "functions=#66ff99",
            "key_types=#66ccff",
            "user_defn=#ff9999",
            "other_kws=#ff99ff",
            "comments=#FF3300",
            "numbers=#FF9900",
            "strings=#ffff99",
            "dollar=#cc33ff",
            "arrow=#ffff99",
            "players=#cc33ff" ]    

# Generate colour mappings from config file

colour_map = dict([line.replace("\n","").split("=") for line in data])

re_patterns = {  'functions' : functions,
                 'key_types' : key_types,
                 'user_defn' : user_defn,
                 'other_kws' : other_kws,
                 'comments'  : comments,
                 'numbers'   : numbers,
                 'strings'   : strings,
                 'dollar'    : dollar,
                 'arrow'     : arrow,
                 'players'   : players }


# Weightings (heavier get checked last)

tag_weights = [['numbers'],
               ['key_types','functions','user_defn','other_kws','dollar','arrow','players'],
               ['comments'],
               ['strings']]

# Font Data

DEFAULT_FONT = "Ubuntu Mono"
