import re

reg = r"\A@\S+"
txt = "@livefunction"

print re.findall(reg, txt)
