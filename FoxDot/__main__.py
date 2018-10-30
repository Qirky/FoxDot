"""
    FoxDot __main__.py
    ------------------

    Use FoxDot's interface by running this as a Python script, e.g.
    python __main__.py or python -m FoxDot if you have FoxDot correctly
    installed and Python on your path.

"""

from __future__ import absolute_import, division, print_function
from lib import FoxDotCode, handle_stdin
from lib.Workspace import workspace
#i removed the dots before lib

import sys

# If we are getting command line input

if sys.argv[-1] == "--pipe":

    # Set up pipe

    handle_stdin()

else:

    # Start the gui

    FoxDot = workspace(FoxDotCode).run()
