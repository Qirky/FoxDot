"""

    parse.py

    This module contains functions and RegEx for identifying FoxDot syntax

"""

re_player_object  = r'\w+ >> \w+\('
re_sample_player  = r'\w+ \$ .*?\n'
re_when_statement = r'(when .*:(\n(else:\s*?\n)?(    )+\S.*)+)'
re_any_assignment = r".*=.*"

re_new_instance  = r"%s\s*=\s*\w*?\("
re_new_reference = r"%s\s*=\s*"

closing_brackets = { "(" : "()",
                     ")" : "()",
                     "[" : "[]",
                     "]" : "[]",
                     "{" : "{}",
                     "}" : "{}" }

def brackets(string, start=0, style="()"):
    """ Returns the indices of the first bracket and its closing """

    if type(string) != str:
        string = "".join(string)

    num = 0
    open_br, closed_br = None, None
    
    for i in range(start, len(string)):
        
        if string[i] == style[0] :

            if open_br is None:

                open_br = i

            num += 1

        if string[i] == style[1] :

            num -= 1

        if num == 0:

            if open_br is not None:

                closed_br = i + 1

                break

    if num == 0:

        return open_br, closed_br

    else:

        return None, None


def find_nested_groups(string):

    i = 0
    data = []
    
    bracket_styles = {"()" : list,
                      "[]" : tuple,
                      "{}" : str }

    while i < len(string):

        char = string[i]

        if char in "([{":
            
            a, b = brackets(string, i, closing_brackets[char])

            char = bracket_styles[string[a]+string[b-1]](string[a+1:b-1])

            i = b - 1

        data.append(char)

        i += 1
        
    return data              



    
