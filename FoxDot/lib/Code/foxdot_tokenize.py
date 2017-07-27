##'''
##    Code to allow Python files written in FoxDot to account for the "when"
##    statements. These files are given a header of `# coding: FoxDot` and
##    should then be automatically tokenized.
##
##    Source: http://stackoverflow.com/questions/214881/can-you-add-new-statements-to-pythons-syntax
##
##'''
##
##from __future__ import absolute_import, division, print_function
##
##try:
##    import new
##except ImportError:
##    from types import ModuleType
##    new = ModuleType
##
##import tokenize
##import codecs, cStringIO, encodings
##from encodings import utf_8
##
##def read(file):
##    ''' Converts a file-like object into FoxDot code '''
##    return tokenize.untokenize(translate(file.readline))
##
##def translate(readline):
##    ''' Searches for any FoxDot syntax (currently only when statements) '''
##    tokens = []
##    startline = 0
##    thisline  = 0
##    compiling = False
##    justcompiled = False
##    
##    expr      = False # If we have defined the expression
##    do        = False # If we have defined the do method
##    elsedo    = False # If we have defined the elsedo method
##
##    dedent    = False
##    indent    = False
##
##    # Iterate through all of the tokens in a file
##    for type, name, start, end, line in tokenize.generate_tokens(readline):
##        
##        if compiling:
##                    
##            if start[0] == startline and not expr:
##
##              # Get the rest of the statement
##
##              tokens.insert(-1, (tokenize.STRING,
##                                 line.strip().replace('when', '').replace(':','')))
##              
##              tokens.append((tokenize.OP, '.'))
##              tokens.append((tokenize.NAME, 'do'))
##              tokens.append((tokenize.OP, '('))
##              tokens.append((tokenize.OP, ')'))
##
##              # We have define the expression
##
##              expr = True
##
##            # New line in the statement
##
##            elif start[0] > thisline:
##
##                thisline = start[0]
##
##                if type == tokenize.INDENT:
##
##                    indent = True
##                    dedent = False
##
##                elif type == tokenize.DEDENT:
##
##                    dedent = True
##                    indent = False
##
##                # Add line that have been indented
##
##                if indent == True:
##
##                    # We have the right bracket already, so insert before
##
##                    if line.strip() != "":
##
##                        tokens.insert(-1, (tokenize.STRING, repr(line.strip())))
##                        tokens.insert(-1, (tokenize.OP, ','))
##
##            # We've gone back an indendatoin level
##
##            elif dedent == True:
##
##                if type == tokenize.NAME and name == 'else':
##
##                    tokens.append((tokenize.OP, '.'))
##                    tokens.append((tokenize.NAME, 'elsedo'))
##                    tokens.append((tokenize.OP, '('))
##                    tokens.append((tokenize.OP, ')'))
##
##                    elsedo = True
##                    dedent = False
##
##                else:
##
##                    dedent = False
##                    compiling = False
##
##                    # We've now exited the when statement.
##
##                    tokens.append((tokenize.NEWLINE, '\n'))
##                    tokens.append((tokenize.NL, '\n'))
##                    tokens.append((type, name))
##
##                    for token, name in tokens:
##
##                        yield token, name
##
##                    tokens = []
##
##        else:
##
##            # If we have a when statement, start to compile
##            if type ==tokenize.NAME and name =='when':
##
##                tokens.append((tokenize.NAME, '__when__'))
##                tokens.append((tokenize.OP, '('))
##                tokens.append((tokenize.NAME, 'lambda'))
##                tokens.append((tokenize.OP, ':'))
##                tokens.append((tokenize.OP, ')'))
##
##                compiling = True
##                
##                thisline = startline = start[0]
##
##            else:
##
##                yield type,  name
##
##def _test(filename):
##    ''' Prints out the converted contents of a file '''
##    f = open(filename)
##    data = tokenize.untokenize(translate(f.readline))
##    f.close()
##    print(data)
##
##def _import(filename):
##    ''' Returns a 'translated' version of a Python file into FoxDot as a module  '''
##    mod = new.module(filename)
##    f = open(filename)
##    data = tokenize.untokenize(translate(f.readline))
##    exec(data, mod.__dict__)
##    return mod
##
##class StreamReader(utf_8.StreamReader):
##    def __init__(self, *args, **kwargs):
##        codecs.StreamReader.__init__(self, *args, **kwargs)
##        data = tokenize.untokenize(translate(self.stream.readline))
##        self.stream = cStringIO.StringIO(data)
##
##def search_function(s):
##    ''' Allows "FoxDot" files to be imported properly '''
##    if s!='foxdot': return None
##    utf8=encodings.search_function('utf8') # Assume utf8 encoding
##    return codecs.CodecInfo(
##        name='foxdot',
##        encode = utf8.encode,
##        decode = utf8.decode,
##        incrementalencoder=utf8.incrementalencoder,
##        incrementaldecoder=utf8.incrementaldecoder,
##        streamreader=StreamReader,
##        streamwriter=utf8.streamwriter)
##
##codecs.register(search_function)
##
##if __name__ == "__main__":
##
##    _test("test.py")
