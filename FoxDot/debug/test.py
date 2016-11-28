import re
from random import shuffle

re_nests  = r"\((.*?)\)"
re_square = r"\[.*?\]"
re_curly  = r"\{.*?\}"
re_chars  = r"[^[\](){}]"
string = "x-o([-o]-)"

desired = "(-[o-])o-x"

pairs = {"(":")",
         ")":"(",
         "[":"]",
         "]":"[",
         "{":"}",
         "}":"{"}

l = list(string)

print desired
l.reverse()
for i, char in enumerate(l):
    if char in pairs.keys():
        l[i] = pairs[char]
new =  "".join(l)

line = "bd >> play('" + string +"', dur=1/2)"

i = line.index(string)
j = i + len(string)

print line[:i] + new + line[j:]

##
### 1. Get all the characters out in order
##
##chars = re.findall(re_chars, string)
##
##empty = re.sub(re_chars, "{}", string)
##
### 2. Shuffle
##
##shuffle(chars)
##
### 3. replace
##
##output = empty.format(*chars)
##
##print line
##print line.replace(string, output)
##
##print output # this is a pure string
