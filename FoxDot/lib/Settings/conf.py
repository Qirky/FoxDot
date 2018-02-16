import os.path
import sys

PY_VERSION = sys.version_info[0]

if PY_VERSION == 2:

    FileNotFoundError = IOError

filename = os.path.join(os.path.dirname(__file__), "conf.txt")

try:
    
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if not line[0] == "#":
            code = compile(line.strip(), "FoxDot", "exec")
            exec(code, globals())

except FileNotFoundError:

    # Settings
    # ------------------
    ADDRESS='localhost'
    PORT=57110
    PORT2=57120
    FONT='Consolas'
    SUPERCOLLIDER=""
    BOOT_ON_STARTUP=False
    SC3_PLUGINS=False
    MAX_CHANNELS=2
    SAMPLES_DIR=""
    GET_SC_INFO=True
    USE_ALPHA=False
    ALPHA_VALUE=0.8

    # Text colours
    # ------------------

    plaintext='#ffffff'
    background='#1a1a1a'
    functions='#bf4acc'
    key_types='#29abe2'
    user_defn='#29abe2'
    other_kws='#49db8b'
    comments='#666666'
    numbers='#e89c18'
    strings='#eae02a'
    dollar='#ec4e20'
    arrow='#eae02a'
    players='#ec4e20'