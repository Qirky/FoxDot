import re

var = "a"

line = "a = var([0,2])"

after = line = re.sub(r"%s\s*=\s*[Vv]ar\(" % var ,"%s.update(" % var, line)

print after
