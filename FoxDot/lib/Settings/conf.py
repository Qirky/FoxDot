import os.path

filename = os.path.join(os.path.dirname(__file__), "conf.txt")
with open(filename) as f:
    lines = f.readlines()
for line in lines:
    if not line[0] == "#":
        code = compile(line.strip(), "FoxDot", "exec")
        exec(code, globals())
