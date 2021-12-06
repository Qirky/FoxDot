from __future__ import absolute_import, division, print_function

import os
import sys

# Anything that needs to be updated

PY_VERSION = sys.version_info[0]

# Any Py2to3

if PY_VERSION == 2:

    range = xrange
    input = raw_input

else:

    from importlib import reload

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
FOXDOT_HELLO = os.path.realpath(FOXDOT_ROOT + "/lib/Workspace/img/hello.txt")
FOXDOT_STARTUP_PATH = os.path.realpath(FOXDOT_ROOT + "/lib/Custom/startup.py")
FOXDOT_SND   = os.path.realpath(FOXDOT_ROOT + "/snd/")
FOXDOT_LOOP  = os.path.realpath(FOXDOT_ROOT + "/snd/_loop_/")

SCLANG_EXEC   = 'sclang.exe' if SYSTEM == WINDOWS else 'sclang'
SYNTHDEF_DIR  = os.path.realpath(FOXDOT_ROOT + "/osc/scsyndef/")
EFFECTS_DIR   = os.path.realpath(FOXDOT_ROOT + "/osc/sceffects/")
ENVELOPE_DIR  = os.path.realpath(FOXDOT_ROOT + "/osc/scenvelopes/")
TUTORIAL_DIR  = os.path.realpath(FOXDOT_ROOT + "/demo/")
RECORDING_DIR = os.path.realpath(FOXDOT_ROOT + "/rec/")

FOXDOT_OSC_FUNC     = os.path.realpath(FOXDOT_ROOT + "/osc/OSCFunc.scd")
FOXDOT_STARTUP_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Startup.scd")
FOXDOT_BUFFERS_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Buffers.scd")
FOXDOT_EFFECTS_FILE = os.path.realpath(FOXDOT_ROOT + "/osc/Effects.scd")
FOXDOT_INFO_FILE    = os.path.realpath(FOXDOT_ROOT + "/osc/Info.scd")
FOXDOT_RECORD_FILE  = os.path.realpath(FOXDOT_ROOT + "/osc/Record.scd")
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

try:
    reload(conf) # incase of a reload
except NameError:
    from . import conf

FOXDOT_CONFIG_FILE  = conf.filename
    
ADDRESS                   = conf.ADDRESS
PORT                      = conf.PORT
PORT2                     = conf.PORT2
FONT                      = conf.FONT
SC3_PLUGINS               = conf.SC3_PLUGINS
MAX_CHANNELS              = conf.MAX_CHANNELS
GET_SC_INFO               = conf.GET_SC_INFO
USE_ALPHA                 = conf.USE_ALPHA
ALPHA_VALUE               = conf.ALPHA_VALUE
MENU_ON_STARTUP           = conf.MENU_ON_STARTUP
TRANSPARENT_ON_STARTUP    = conf.TRANSPARENT_ON_STARTUP
RECOVER_WORK              = conf.RECOVER_WORK
CHECK_FOR_UPDATE          = conf.CHECK_FOR_UPDATE
LINE_NUMBER_MARKER_OFFSET = conf.LINE_NUMBER_MARKER_OFFSET
AUTO_COMPLETE_BRACKETS    = conf.AUTO_COMPLETE_BRACKETS
CPU_USAGE                 = conf.CPU_USAGE
CLOCK_LATENCY             = conf.CLOCK_LATENCY
FORWARD_ADDRESS           = conf.FORWARD_ADDRESS
FORWARD_PORT              = conf.FORWARD_PORT

if conf.SAMPLES_DIR is not None and conf.SAMPLES_DIR != "":

    FOXDOT_SND = os.path.realpath(conf.SAMPLES_DIR)

# Recreate info file from template
try:
    with open(FOXDOT_INFO_FILE+".template", "r") as fread:
        # Delete info file only if template file exists
        if os.path.isfile(FOXDOT_INFO_FILE):
            os.remove(FOXDOT_INFO_FILE)

        content = fread.read()
        content = content.replace("<FOXDOT_ROOT>", f"'{FOXDOT_ROOT}'")
        content = content.replace("<FOXDOT_SND>", f"'{FOXDOT_SND}'")
        with open(FOXDOT_INFO_FILE, "w") as f:
            f.write(content)
except FileNotFoundError:
    pass

def get_timestamp():
    import time
    return time.strftime("%Y%m%d-%H%M%S")

# Name of SamplePlayer and LoopPlayer SynthDef

class _SamplePlayer:
    names = ('play1', 'play2',)
    def __eq__(self, other):
        return other in self.names
    def __ne__(self, other):
        return other not in self.names

class _LoopPlayer:
    names = ("loop", "gsynth", 'stretch')
    def __eq__(self, other):
        return other in self.names
    def __ne__(self, other):
        return other not in self.names

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
