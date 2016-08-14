import os
import sys

# Check Python Version TODO

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
SCLANG_EXEC  = 'sclang.exe' if SYSTEM == WINDOWS else 'sclang'
OSC_FUNC     = "/FoxDot/SCLang/OSCFunc.scd"

# Open custom settings

with open(os.path.join(FOXDOT_ROOT, 'FoxDot', 'Settings', 'conf.txt')) as f:
    _conf = dict([line.replace("\n","").split("=",1) for line in f.readlines() if "=" in line])

# Set Environment Variables

SC_DIRECTORY  = _conf['SUPERCOLLIDER']
ADDRESS       = _conf['ADDRESS']
PORT          = _conf['PORT']
FONT          = _conf['FONT']

# Colours

class COLOURS:
    plaintext  = _conf['plaintext']
    background = _conf['background']
    functions  = _conf['functions']
    key_types  = _conf['key_types']
    user_defn  = _conf['user_defn']
    other_kws  = _conf['other_kws']
    comments   = _conf['comments']
    numbers    = _conf['numbers']   
    strings    = _conf['strings']
    dollar     = _conf['dollar']  
    arrow      = _conf['arrow']   
    players    = _conf['players']

# Buffer Details



