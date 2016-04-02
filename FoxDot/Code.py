from __future__ import division

import re
from types import CodeType
func_type = type(lambda: None)
from traceback import format_exc as error_stack

debug = -1

# --------------------- Handling Code

def toCompile(expression):
    return expression, "FoxDot", "exec"

def execute(code, verbose=True):

    """ Takes a string of foxdot code and calls toPython()
`       and exectues the returned python string in our
        global namespace """

    try:

        if type(code) != CodeType:

            code = toPython( code, verbose )

        exec code in globals()

    except:

        print error_stack()

        raise # raise the error to any foxdot code that executes foxdot code

    return


def toPython( code, verbose ):

    """ Converts any FoxDot code to its equivalent in Python.
        Prints the code to the console if the verbose flag is set to True """

    # Look for any 'when' statements

    code = GetWhenStatements( code )

    # Look for FoxDot syntax for new players

    code = GetPlayerAssignments( code )

    # Convert any re-assignment of players already playing to update methods
    
    code = GetAssignmentsAsUpdates( code )

    if not code: return ""

    # Print out the code to the console

    if verbose:

        print stdout( code ) 

    # 5. Convert to python code to be executed

    raw_python = compile(code, 'FoxDot', 'exec')

    return raw_python

def GetWhenStatements( code ):
    """ Finds any when statements and converts them to a string that creates TempoClock.When objects """

    statements = [ match[0] for match in re.findall(r'(when .*:(\n(else:\s*?\n)?(    )+\S.*)+)', code) ]
    
    for s in statements:
        key = re.search(r'when (.*?):', s).group(1).replace('"','\"')
        new = s.replace("when ", "if ").replace('"','\"').split("\n")
        when = "Clock.when(\"%s\", %s )\n" % (key,str(new))
        code = code.replace(s, when)

    return code

def GetPlayerAssignments( code ):
    """ Replaces any FoxDot code with Python code """

    # RegEx for instruments constructed using VAR >> INSTRUMENT()

    instruments = re.findall(r'\w+ >> \w+\(', code )

    # RexEx for samples constructed using VAR $ STRING

    samples = re.findall(r'\w+ \$ .*?\n', code )

    assignments = instruments + samples

    for n in range( len( assignments ) ):

        # Find out what kind of player we have

        if ">>" in assignments[n]:
            
            var, op, SynthDef = assignments[n].replace("(","").split()

        elif "$" in assignments[n]:

            SynthDef = "sample_player"

            var, op, pattern  = assignments[n].replace("\n","").split(' ', 2)

        # Find the object arguments and the index of the string at which it ends

        start = code.index(assignments[n]) + len(assignments[n]) - 1

        try:

            end = code.index(assignments[n+1])

        except:

            end = None

        data = code[start:end]
        
        # Loop through the arguments to find the enclosing brackets

        Arguments, index = enclosing_brackets( data )

        # Add the sample player pattern

        if SynthDef == "sample_player":

           Arguments.append( pattern )

        # Check for any information AFTER the init

        Methods = data[index:].rstrip()
          
        # Replace "old" code with new

        old_code = code[code.index(assignments[n]):end]

        if SynthDef == "sample_player":

            new_code = "%s = SamplePlayer( %s )\n%s\n" % (var, ", ".join(Arguments), Methods)

        else:

            new_code = "%s = Player('%s', %s )%s\n" % (var, SynthDef, ", ".join(Arguments), Methods)

        code = code.replace(old_code, new_code)

    return code

# Formatting and cleaning code funcrtions below

def GetAssignmentsAsUpdates( code ):
    """ Finds any attempt to re-assign a player while playing and reformats the arguments """

    ns = globals()

    # look for any lines starting with a = b

    lines = code.split("\n")

    new_code = []

    for line in lines:

        assignment = re.match(r".*=.*", line.strip())

        if assignment:

            var = line.split('=', 1)[0].strip()

            # See if A is a Player instance
            
            try:

                # Case 1: Object is Player

                if ns[var].isplaying:

                    # Re-Format #

                    before = line                    

                    after = line = re.sub(r"%s\s*=\s*(Sample)?Player\(" % var ,"%s.update(" % var, line)

                    if before == after:

                        raise RuntimeWarning("Variable '%s' can only be assigned to a Player or SamplePlayer object while playing" % var)

                # Case 2: Object is TimeVar

                if ns[var].isTimeVar:

                    # Re-Format #

                    before = line                    

                    after = line = re.sub(r"%s\s*=\s*[Vv]ar\(" % var ,"%s.update(" % var, line)

                    if before == after:

                        raise RuntimeWarning("Variable '%s' can only be assigned to a new TimeVar object" % var)

            except (KeyError, AttributeError):

                pass # Object isn't a Player / TimeVar

        new_code.append( line )

    code = "\n".join(new_code)

    return code

def enclosing_brackets(string):

    open_b = 0
    
    for i in range(len(string)):
        if string[i] == "(" :
            open_b += 1
        if string[i] == ")" :
            open_b -= 1
        if open_b == 0:
            break

    bracketed_string = string[1:i]

    close = i + 1

    open_b = 0
    last_index = 0
    arguments = []

    # Separate on commas not inside brackets

    for i in range(len(bracketed_string)):

        if bracketed_string[i] in ["(","[","{"]:
            open_b += 1
        if bracketed_string[i] in [")","]","}"]:
            open_b -= 1

        # if we find a comma when we aren't in any brackets, split

        if (bracketed_string[i] == "," and open_b == 0):

            arguments.append( bracketed_string[last_index:i].strip() )

            last_index = i + 1

        elif i == len(bracketed_string) - 1:

            arguments.append( bracketed_string[last_index:i+1].strip() )

            last_index = i + 1
            
    return arguments, close


# Imitates the Python IDE output style

def stdout(code):

    console_text = code.strip().split("\n")

    return ">>> %s" % "\n>>> ".join(console_text)

