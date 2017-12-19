"""
    FoxDot __main__.py
    ------------------

    Use FoxDot's interface by running this as a Python script, e.g.
    python __main__.py or python -m FoxDot if you have FoxDot correctly
    installed and Python on your path. 

"""

from __future__ import absolute_import, division, print_function

import sys

if sys.version_info[0] == 2:

    ModuleNotFoundError = Exception

try:

    from .lib import FoxDotCode
    from .lib import execute

except(ValueError, ModuleNotFoundError):

    from lib import FoxDotCode
    from lib import execute

# If we are getting command line input

if sys.argv[-1] == "--pipe":

    # Set up pipe

    while True:

        # Read in

        text = input("")
        execute(text, verbose=False, verbose_error=True)

else:

    # Start the gui

    try:

        from .lib.Workspace import workspace

    except(ValueError, ModuleNotFoundError):
        
        from lib.Workspace import workspace

    FoxDot = workspace(FoxDotCode).run()
