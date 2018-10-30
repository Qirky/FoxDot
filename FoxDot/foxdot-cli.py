#!/usr/bin/env python
import os
import cmd

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ACTIVATE_PY = os.path.join(BASE_PATH, ".env", "bin", "activate_this.py")
execfile(ACTIVATE_PY, dict(__file__=ACTIVATE_PY))

from FoxDot import *

class FoxDotConsole(cmd.Cmd):
    prompt = "FoxDot> "
    intro = "LiveCoding with Python and SuperCollider"

    def default(self, line):
        execute(line)

if __name__ == "__main__":
    FoxDotConsole().cmdloop()