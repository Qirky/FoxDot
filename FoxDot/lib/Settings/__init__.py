import os
import sys

# Check for OS -> mac, linux, win

SYSTEM  = 0
WINDOWS = 0
LINUX   = 1
MAC_OS  = 2

if sys.platform.startswith('darwin'):

    SYSTEM = MAC_OS

elif sys.platform.startswith('win'):

    SYSTEM = WINDOWS

elif sys.platform.startswith('linux'):

    SYSTEM = LINUX

# Directory informations

USER_CWD     = os.path.realpath(".")
FOXDOT_ROOT  = os.path.realpath(__file__ + "/../../../")
FOXDOT_ICON  = os.path.realpath(FOXDOT_ROOT + "/lib/Workspace/img/icon" + (".ico" if SYSTEM != LINUX else ".gif"))
FOXDOT_SND   = os.path.realpath(FOXDOT_ROOT + "/snd/")

SCLANG_EXEC  = 'sclang.exe' if SYSTEM == WINDOWS else 'sclang'
SYNTHDEF_DIR = os.path.realpath(FOXDOT_ROOT + "/osc/scsyndef/")
EFFECTS_DIR  = os.path.realpath(FOXDOT_ROOT + "/osc/sceffects/")

FOXDOT_OSC_FUNC     = os.path.realpath(FOXDOT_ROOT + "/osc/OSCFunc.scd")
FOXDOT_STARTUP_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Startup.scd")
FOXDOT_BUFFERS_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Buffers.scd")
FOXDOT_EFFECTS_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Effects.scd")

def GET_SYNTHDEF_FILES():
    return [os.path.realpath(SYNTHDEF_DIR + "/" + path) for path in os.listdir(SYNTHDEF_DIR)]

def GET_FX_FILES():
    return [os.path.realpath(EFFECTS_DIR + "/" + path) for path in os.listdir(EFFECTS_DIR)]

# Set Environment Variables

import conf

if conf.SUPERCOLLIDER == '':

    import tkFileDialog
    import Tkinter

    root = Tkinter.Tk()
    root.withdraw()
    
    sc_dir = tkFileDialog.askdirectory(title="Please Find Your SuperCollider Installation Directory")

    if not sc_dir:

        sys.exit('Please locate SuperCollider and try using FoxDot again')

    root.destroy()

    SC_DIRECTORY = sc_dir

    # Re-write conf file for next use

    conf_fn = os.path.realpath(os.path.dirname(__file__) + "/conf.py")

    with open(conf_fn) as f:

        conflines = f.readlines()

    with open(conf_fn, 'w') as f:

        for line in conflines:

            if 'SUPERCOLLIDER' in line:

                f.write('SUPERCOLLIDER="' + sc_dir + '"\n')

            else:

                f.write(line)
else:

    SC_DIRECTORY  = conf.SUPERCOLLIDER
    
ADDRESS       = conf.ADDRESS
PORT          = conf.PORT
PORT2         = conf.PORT2
FONT          = conf.FONT
SC3_PLUGINS   = conf.SC3PLUGINS
MAX_CHANNELS  = conf.MAX_CHANNELS

# Name of SamplePlayer SynthDef

class _SamplePlayer:
    names = ('play1', 'play2')
    def __eq__(self, other):
        return other in self.names
    def __ne__(self, other):
        return other not in self.names

SamplePlayer = _SamplePlayer()

# Colours

class COLOURS:
    plaintext  = conf.plaintext
    background = conf.background
    functions  = conf.functions
    key_types  = conf.key_types
    user_defn  = conf.user_defn
    other_kws  = conf.other_kws
    comments   = conf.comments
    numbers    = conf.numbers
    strings    = conf.strings
    dollar     = conf.dollar
    arrow      = conf.arrow
    players    = conf.players
