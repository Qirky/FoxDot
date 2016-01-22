import re

# These are the sets of keywords that are used

py_functions = ["if","elif","else","return","def",
                 "and","or","not","is","in","for","as",
                 "while", "class", "import", "print" ]

py_key_types = ["str","int","float","type","repr",
                 "range","open","len","sorted","set",
                 "None","True","False","bool","chr"]

# These are the characters that separate keywords

py_separators = list("[](){},./*+=- \t\n")

# These are the regex patterns

functions = r"" + "$|".join(py_functions) + "$"
key_types = r"" + "$|".join(py_key_types) + "$"
user_defn = r"def (\w)+"
comments  = r"#.*\n+"
numbers   = r"\d+$"
strings   = r"\"\w*\"|\'\w*\'"

# Read config file - TODO error check

with open("config.txt") as f:
    data = f.readlines()

# Generate colour mappings from config file

colour_map = dict([line.replace("\n","").split("=") for line in data])

regex_name = {  'functions' : functions,
                'key_types' : key_types,
                'user_defn' : user_defn,
                'comments'  : comments,
                'numbers'   : numbers,
                'strings'   : strings }

def styletype(word):
    """ Matches the word to it's style tag using RegEx """

    for style in regex_name:

        if re.match(regex_name[style], word):

            return style
