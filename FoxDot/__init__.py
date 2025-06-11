#!/usr/bin/python

"""

FoxDot is a Python library and programming environment that provides a fast and
user-friendly abstraction to the powerful audio-engine, SuperCollider. It comes
with its own IDE, which means it can be used straight out of the box; all you need
is Python and SuperCollider and you're ready to go!

For more information on installation, check out [the guide](http://foxdot.org/installation),
or if you're already set up, you can also find a useful starter guide that introduces the
key components of FoxDot on [the website](http://foxdot.org/).

Please see the [documentation](http://docs.foxdot.org/) for more detailed information on
the FoxDot classes and how to implement them.

Copyright Ryan Kirkbride 2015
"""

from __future__ import absolute_import, division, print_function

from FoxDot.BootManager import Boot

if not Boot.running and Boot.BOOT_ON_STARTUP:
    Boot.start()

from .lib import *

def main():
    """ Function for starting the GUI when importing the library """
    from .lib.Workspace.Editor import workspace
    FoxDot = workspace(FoxDotCode).run()

def Go():
    """ Function to be called at the end of Python files with FoxDot code in to keep
        the TempoClock thread alive. """
    try:
        import time
        while 1:
            time.sleep(100)
    except KeyboardInterrupt:
        execute("Clock.stop()")
        execute("Server.quit()")
        execute("Boot.stop()")
