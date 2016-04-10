"""

    sample_players.py

    This module finds any assignments using the sample player creation syntax:

        name $ string_of_chars

    and converts to:

        name = SamplePlayer(string_of_chars)

"""

import re
import parse

def find( text ):

    assignments = re.findall(parse.re_sample_player, text )

    for n in range( len( assignments ) ):
           
        name, dollar, pattern  = assignments[n].replace("\n","").split(None, 2)

        # Replace "old" code with new

        old_code = assignments[n]

        new_code = "%s = SamplePlayer( %s )\n" % (name, pattern)

        text = text.replace(old_code, new_code)

    return text
