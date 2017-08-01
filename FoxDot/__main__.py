"""
    FoxDot __main__.py
    ------------------

    Use FoxDot's interface by running this as a Python script, e.g.
    python __main__.py or python -m FoxDot if you have FoxDot correctly
    installed and Python on your path. 

"""

from __future__ import absolute_import, division, print_function

try:

    from .lib import FoxDotCode
    from .lib.Workspace import workspace

except ValueError:

    from lib import FoxDotCode
    from lib.Workspace import workspace

FoxDot = workspace(FoxDotCode).run()
