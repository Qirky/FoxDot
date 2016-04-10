"""
    assignments.py

    Checks if any variables that are being assigned a value are already
    in the global namespace. If so, then replaces the assignment with an
    update method. If the update method doesn't exist, or fails, it
    assigns the variable anyway

"""

import re
import parse

def check(code, namespace):

    lines = code.split("\n")

    new_code = []

    for line in lines:

        assignment = re.match(parse.re_any_assignment, line.strip())

        if assignment:

            name = line.split('=', 1)[0].strip()

            if name in namespace:

                if hasattr(namespace[name], "foxdot_object"):

                    line = re.sub(parse.re_sub_foxdot_assignment % name, "%s.update(" % name, line )

        new_code.append(line)

    code = "\n".join(new_code)
    
    return code
