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
OSC_FUNC     = "/lib/SCLang/OSCFunc.scd"

# Set Environment Variables

import conf

SC_DIRECTORY  = conf.SUPERCOLLIDER
ADDRESS       = conf.ADDRESS
PORT          = conf.PORT
PORT2         = conf.PORT2
FONT          = conf.FONT
SC3_PLUGINS   = conf.SC3PLUGINS
MAX_CHANNELS  = conf.MAX_CHANNELS

# Name of SamplePlayer SynthDef

SamplePlayer = 'play'

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
