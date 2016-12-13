"""
    FoxDot __main__.py
    ------------------

    Use FoxDot's interface by running this as a Python script, e.g.
    python __main__.py or python -m FoxDot if you have FoxDot correctly
    installed and Python on your path. 

"""

from lib import *
from lib.Workspace import workspace

# Create the  IDE
FoxDot = workspace()

# This allows the user to access the IDE, an object called FoxDot
FoxDotCode.namespace['FoxDot'] = FoxDot

# And this gives PlayerObjects access to the  IDE too
Player.widget = FoxDot

# This shares the code namespace between Python and the FoxDot IDE
workspace.namespace=FoxDotCode.namespace

# Run the IDE. Stop threads if it exits.

try:

    FoxDot.run()

except (KeyboardInterrupt, SystemExit):

    Clock.stop()

    Server.quit()
