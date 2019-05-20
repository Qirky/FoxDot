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

def boot_supercollider():
    """ Uses subprocesses to boot supercollider from the cli """

    import time
    import platform
    import os
    import subprocess
    import getpass

    try:
        import psutil
    except ImportError:
        os.system("pip install psutil")
        import sys
        sys.exit("Installed psutil, please start FoxDot again.")

    sclangpath = "" #find path to sclang

    thispath = "" #find this path

    thisdir = os.getcwd()

    OS = platform.system()

    username = getpass.getuser()

    if(OS == "Windows"):

        print("OS: Windows")

        sclangloc = os.popen('where /R "C:\\Program Files" sclang.exe').read()

        thiscwd = str(sclangloc)

        ourcwd = thiscwd.replace('\\sclang.exe\n', '')

        def is_proc_running(name):
            for p in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
                #print(p);
                procname = p.info['name'] or \
                     p.info['exe'] and os.path.basename(p.info['exe']) == name or \
                     p.info['cmdline'] and p.info['cmdline'][0] == name
                if(procname.startswith(name)):
                    return True
            return False


        running = (is_proc_running("sclang"))

        if(running == False):
            startup = thisdir+"/FoxDot/startup.scd"
            #os.system("sclang"+startup+" &")
            subprocess.Popen([sclangloc, startup], cwd=ourcwd, shell=True)

    elif(OS == "Linux"):

        print("OS: Linux")

        def is_proc_running(name):
            for p in psutil.process_iter(attrs=["name","cmdline"]):
                #print(p);
                procname = p.info['name'] or \
                     p.info['cmdline'] and p.info['cmdline'][0] == name
                if(procname.startswith(name)):
                    return True


        running = (is_proc_running("sclang"))

        if(running == False):
            startup = thisdir+"/FoxDot/startup.scd"
            #os.system('sclang "/home/foxdot/Desktop/FoxDot-Cross-Platform/FoxDot/startup.scd" &') #fuctional
            os.system("sclang "+startup+" &")


    else:
        print("Operating system unrecognised")
        #Potentially get the user to choose their OS from a list?
        #Then run the corresponding functions

import sys

if "--boot" in sys.argv:

    boot_supercollider()

    sys.argv.remove("--boot")

from .lib import *

def main():
    """ Function for starting the GUI when importing the library """
    FoxDot = Workspace.workspace(FoxDotCode).run()

def Go():
    """ Function to be called at the end of Python files with FoxDot code in to keep
        the TempoClock thread alive. """
    try:
        import time
        while 1:
            time.sleep(100)
    except KeyboardInterrupt:
        return
