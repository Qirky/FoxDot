from __future__ import absolute_import, division, print_function

import os
import sys

# Anything that needs to be updated

PY_VERSION = sys.version_info[0]

# Any Py2to3

if PY_VERSION == 2:

    range = xrange
    input = raw_input

# Check for OS -> mac, linux, win

SYSTEM  = 0
WINDOWS = 0
LINUX   = 1
MAC_OS  = 2

if sys.platform.startswith('darwin'):

    SYSTEM = MAC_OS

    # Attempted fix for some Mac OS users

    try:
        import matplotlib
        matplotlib.use('TkAgg')
    except ImportError:
        pass

elif sys.platform.startswith('win'):

    SYSTEM = WINDOWS

elif sys.platform.startswith('linux'):

    SYSTEM = LINUX

# Directory informations

USER_CWD     = os.path.realpath(".")
FOXDOT_ROOT  = os.path.realpath(__file__ + "/../../../")
FOXDOT_ICON  = os.path.realpath(FOXDOT_ROOT + "/lib/Workspace/img/icon.ico")
FOXDOT_ICON_GIF = os.path.realpath(FOXDOT_ROOT + "/lib/Workspace/img/icon.gif")
FOXDOT_SND   = os.path.realpath(FOXDOT_ROOT + "/snd/")
FOXDOT_LOOP  = os.path.realpath(FOXDOT_ROOT + "/snd/_loop_/")

SCLANG_EXEC   = 'sclang.exe' if SYSTEM == WINDOWS else 'sclang'
SYNTHDEF_DIR  = os.path.realpath(FOXDOT_ROOT + "/osc/scsyndef/")
EFFECTS_DIR   = os.path.realpath(FOXDOT_ROOT + "/osc/sceffects/")
ENVELOPE_DIR  = os.path.realpath(FOXDOT_ROOT + "/osc/scenvelopes/")
TUTORIAL_DIR  = os.path.realpath(FOXDOT_ROOT + "/demo/")

FOXDOT_OSC_FUNC     = os.path.realpath(FOXDOT_ROOT + "/osc/OSCFunc.scd")
FOXDOT_STARTUP_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Startup.scd")
FOXDOT_BUFFERS_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Buffers.scd")
FOXDOT_EFFECTS_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Effects.scd")
FOXDOT_INFO_FILE    = os.path.realpath(FOXDOT_ROOT + "/osc/Info.scd")
FOXDOT_TEMP_FILE    = os.path.realpath(FOXDOT_ROOT + "/lib/Workspace/tmp/tempfile.txt")

# If the tempfile doesn't exist, create it

if not os.path.isfile(FOXDOT_TEMP_FILE):
    try:
        with open(FOXDOT_TEMP_FILE, "w") as f:
            pass
    except FileNotFoundError:
        pass

def GET_SYNTHDEF_FILES():
    return [os.path.realpath(SYNTHDEF_DIR + "/" + path) for path in os.listdir(SYNTHDEF_DIR)]

def GET_FX_FILES():
    return [os.path.realpath(EFFECTS_DIR + "/" + path) for path in os.listdir(EFFECTS_DIR)]

def GET_TUTORIAL_FILES():
    return [os.path.realpath(TUTORIAL_DIR + "/" + path) for path in sorted(os.listdir(TUTORIAL_DIR))]

# Set Environment Variables

from . import conf

FOXDOT_CONFIG_FILE  = conf.filename
    
ADDRESS       = conf.ADDRESS
PORT          = conf.PORT
PORT2         = conf.PORT2
FONT          = conf.FONT
SC3_PLUGINS   = conf.SC3_PLUGINS
MAX_CHANNELS  = conf.MAX_CHANNELS
GET_SC_INFO   = conf.GET_SC_INFO
USE_ALPHA     = conf.USE_ALPHA
ALPHA_VALUE   = conf.ALPHA_VALUE

if conf.SAMPLES_DIR is not None and conf.SAMPLES_DIR != "":

    FOXDOT_SND = os.path.realpath(conf.SAMPLES_DIR)

# Name of SamplePlayer and LoopPlayer SynthDef

class _SamplePlayer:
    names = ('play1', 'play2')
    def __eq__(self, other):
        return other in self.names
    def __ne__(self, other):
        return other not in self.names

class _LoopPlayer:
    name = "loop"
    def __eq__(self, other):
        return other == self.name
    def __ne__(self, other):
        return other != self.name

class _MidiPlayer:
    name = "MidiOut"
    def __eq__(self, other):
        return other == self.name
    def __ne__(self, other):
        return other != self.name

SamplePlayer = _SamplePlayer()
LoopPlayer   = _LoopPlayer()
MidiPlayer   = _MidiPlayer()


# OSC Information

OSC_MIDI_ADDRESS = "/foxdot_midi"

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
