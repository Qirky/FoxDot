"""

    player_objects.py

    This module finds any assignments using the player creation syntax:

        name >> SynthDef(degree, kwargs)

    and converts to:

        name = Player("SynthDef", degree, kwargs)

"""

import re
import parse

def find( text ):

    assignments = re.findall(parse.re_player_object, text )

    for n in range( len( assignments ) ):
           
        name, arrows, SynthDef = assignments[n].replace("(","").split()

        # Get the indices of the enclosing brackets

        start = text.index(assignments[n])

        b1, b2 = parse.brackets(text, start)
        
        # Arguments for the players are just the contents of the brackets

        args = text[b1+1:b2-1]        
          
        # Replace "old" code with new

        old_code = assignments[n] + args + ")"

        new_code = "%s = Player('%s', %s )" % (name, SynthDef, args)

        text = text.replace(old_code, new_code)

    return text
