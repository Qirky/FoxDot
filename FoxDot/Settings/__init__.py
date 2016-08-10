import os
import sys

# Check Python Version TODO

# Check for OS

SYSTEM = sys.platform

# Directory informations

USER_CWD     = os.path.realpath(".")
FOXDOT_ROOT  = os.path.realpath(__file__ + "/../../../")
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



