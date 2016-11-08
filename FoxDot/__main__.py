from __init__ import *

""" IDE """

from Interface import FoxDot
FoxDot.namespace=FoxDotCode.namespace

try:
    
    fx_ide = FoxDot()        
    fx_ide.run()

    Clock.stop()
    Server.quit()
    
except (KeyboardInterrupt, SystemExit):

    Clock.stop()
    Server.quit()
