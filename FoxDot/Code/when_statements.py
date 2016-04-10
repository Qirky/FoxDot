"""

    when_statements.py

    This module is used to process any when statements in FoxDot code.

"""

import re
import parse

def find( text ):
    """ Finds any when statements and converts them to a string that creates TempoClock.When objects """

    statements = [ match[0] for match in re.findall(parse.re_when_statement, text) ]
    
    for s in statements:
        
        key = re.search(r'when (.*?):', s).group(1).replace('"','\"')
        
        new = s.replace("when ", "if ").replace('"','\"').split("\n")
        
        when = "Clock.when(\"%s\", %s )\n" % (key, str(new))
        
        text = text.replace(s, when)

    return text
