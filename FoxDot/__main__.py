"""
    FoxDot __main__.py
    ------------------

    Use FoxDot's interface by running this as a Python script, e.g.
    python __main__.py or python -m FoxDot if you have FoxDot correctly
    installed and Python on your path. 

"""

from lib import FoxDotCode
from lib.Workspace import workspace

##import sys
##
##if sys.argv[1] == "-f":
##
##    f = sys.argv[2]

FoxDot = workspace(FoxDotCode).run()
