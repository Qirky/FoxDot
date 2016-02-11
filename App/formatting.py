import re

# RegEx Group 1
user_defn = r"(?<=def )(\w+)"
players   = r"(?<=>> )(\w+)"
comments  = r"#.*"
numbers   = r"(?<![a-zA-Z])\d+"
strings   = r"\".*?\"|\'.*?\'"
dollar    = r"\s\$\s?"
arrow     = r"\s>>\s?"

foxdot_kw = ["var","Var","Clock","default_scale", "group", "Group", "Scale","inf","Inf"]

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

try:
    
    with open("FoxDot/Patterns.py") as f:

        data = f.readlines()

    for line in data:

        match = userdefined(line)

        if match:

            foxdot_kw.append(match)
            
except:

    pass


# Python keywords used in RegEx Group 2

py_indent_kw = ["for","if","elif","else","def","while","class","try","except","when"]

py_functions = ["if","elif","else","return","def","print","when",
                 "and","or","not","is","in","for","as","with",
                 "while", "class", "import", "try","except"]

py_key_types = foxdot_kw + ["str","int","float","type","repr",
                             "range","open","len","sorted","set",
                             "None","True","False","bool","chr",
                             "help","exit","xrange","isintstance"] 

py_separators = list("[](){},./*+=- \t\n")
py_whitespace = list(" \t\n\r\f\v")

left_b = list("([{")
right_b = list(")]}")
brackets = dict([(right_b[i],left_b[i]) for i in range(3)])
tabsize = 4

# RegEx Group 2

functions = r"(?<![a-zA-Z])(" + "|".join(py_functions) + ")(?![a-zA-Z])"
key_types = r"(?<![a-zA-Z])(" + "|".join(py_key_types) + ")(?![a-zA-Z])"

# Load Default Colour Values

try:

    with open("config.txt") as f:

        data = f.readlines()

except:

    data = ["plaintext=#ffffff",
            "background=#4d4d4d",
            "functions=#66ff99",
            "key_types=#66ccff",
            "user_defn=#ff9999",
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
                 'comments'  : comments,
                 'numbers'   : numbers,
                 'strings'   : strings,
                 'dollar'    : dollar,
                 'arrow'     : arrow,
                 'players'   : players }
    
