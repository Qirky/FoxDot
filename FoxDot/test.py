import re

var = "p"

line = "p = Player('pads')"

print re.sub(r"%s\s*=\s*(Sample)?Player\(" % var ,"ryan.update(", line)
