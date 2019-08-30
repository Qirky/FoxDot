from __future__ import absolute_import

# Check wx import - os.system("pip import wxpython and quit?")

try:
    import wx
except ImportError:
    import sys
    sys.exit("Error: wxPython is required to run FoxDot in simple mode. Install by running pip install wxpython.")

from .SimpleEditor import *