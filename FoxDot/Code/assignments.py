"""
    assignments.py

    Checks if any variables that are being assigned a value are already
    in the global namespace. If so, then replaces the assignment with an
    update method. 

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

                    # 1. Get contents of any brackets (if any)

                    if re.search(r"\s*=\s*\w*?\(", line):

                        pattern = parse.re_new_instance
                        sub     = "%s.update("
                        end     = ""

                    else:

                        pattern = parse.re_new_reference
                        sub     = "%s.update("
                        end     = ")"

                    # print parse.re_sub_foxdot_assignment % name

                    line = re.sub(pattern % name, sub % name, line ) + end

        new_code.append(line)

    code = "\n".join(new_code)
    
    return code
