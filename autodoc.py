import inspect
import pydoc
import os.path
import os

# Packages / modules to exclude

EXC_PACKAGES = []
EXC_MODULES  = []

def pkgname(pkg):
    return pkg.replace('.', '\\')

def getdetails(function, name=None):
    ''' returns a string "function(args)" '''

    # Pattern decorators have this attribute

    argspec = function.argspec if hasattr(function, 'argspec') else inspect.getargspec(function)

    args     = argspec.args
    defaults = argspec.defaults if argspec.defaults is not None else ()

    # Put defaults with arguments
    for i in range(1, len(args)+1):
        if i <= len(defaults):
            value = defaults[-i]
            if inspect.isfunction(value):
                value = value.__name__
            args[-i] = (args[-i], value)
        else:
            args[-i] = (args[-i],)

    output =  ['='.join((str(a) for a in arg)) for arg in args]

    # Add any *args or **kwargs
    if argspec.varargs is not None:
        output.append('*' + argspec.varargs)

    if argspec.keywords is not None:
        output.append('**' + argspec.keywords)
        
    return (function.__name__ if name is None else name) + '(' + ', '.join(output) + ')'

class GenerateDocs:
    def __init__(self, package, dir='docs'):

        self.package = package
        self.name    = package.__name__
        self.root    = os.path.dirname(self.package.__file__)
        self.dir     = dir

        # Don't use duplicates

        EXC_PACKAGES.append(self.package)

        # Create a folder to write the docs into

        if not os.path.isdir(self.dir):

            self.makedir(self.dir)
        
        self.modules     = []
        self.subpackages = []

        for name, item in sorted(vars(self.package).items()):

            if self.issubpackage(item):

                if item not in EXC_PACKAGES:

                    self.subpackages.append(GenerateDocs(item, os.path.join(self.dir, pkgname(item.__name__))))

            elif self.ismodule(item):

                if item not in EXC_MODULES:

                    self.modules.append(ModuleDoc(item))

    def __repr__(self):
        return '<doc for ' + self.name + '>'
                        
    def write(self):
        ''' Generate markdown for the package '''
        for module in self.modules:

            module.write(self.dir)

        for package in self.subpackages:

            package.write()

    def makedir(self, path):
        try:
            os.mkdir(path)
        except:
            self.makedir(os.path.dirname(path))
            os.mkdir(path)
        return

    def ismodule(self, module):
        if inspect.ismodule(module) and hasattr(module, '__file__'):
            return self.inpackage(module.__file__)
        else:
            return False

    def issubpackage(self, module):
        if inspect.ismodule(module) and hasattr(module, '__file__'):
            return self.validfile(module.__file__) and os.path.basename(module.__file__) == '__init__.pyc'
        else:
            return False
                
    def validfile(self, path):
        return self.root in os.path.dirname(path)

    def inpackage(self, path):
        return self.root == os.path.dirname(path)

class ModuleDoc:

    def __init__(self, module, dir=''):

        self.module    = module
        self.title     = module.__name__
        self.docstring = inspect.getdoc(module)
        self.file      = None
        self.filename  = self.title + '.md'

        EXC_MODULES.append(self.module)

        self.classes   = {}
        self.functions = {}
        self.data      = {}

        # Iterate over the items defined in module

        for name, item in vars(self.module).items():

            if inspect.getmodule(item) == self.module:

                # Classes

                if inspect.isclass(item):

                    # Ignore private classes

                    if not name.startswith('__'):

                        docstring = inspect.getdoc(item)

                        methods = {getdetails(method): inspect.getdoc(method) for _, method in inspect.getmembers(item) if inspect.ismethod(method) }

                        try:

                            name = getdetails(item.__init__, name)

                        except:

                            name = name + '(self)'

                        self.classes[name] = ClassDoc(docstring, methods)

                # Functions

                elif inspect.isfunction(item):

                    name = getdetails(item, name)

                    self.functions[name] = DataDoc(inspect.getdoc(item))

                # Data
                
                elif pydoc.isdata(item):

                    name = name + " = " + inspect.cleandoc(pydoc.TextDoc().docother(item))

                    self.data[name] = ''

    def __repr__(self):
        return "<doc for {}>".format(self.title)

    def _write_title(self):
        self.file.write('# `{}`\n\n'.format(self.title))
        self.file.write('{}\n\n'.format(self.docstring))

    def _write_section(self, header, level=3):
        self.file.write('## {}\n\n'.format(header.title()))
        for name, doc in sorted(self.__dict__[header].items()):
            self.file.write('#' * level + ' `{}`\n\n'.format(name))
            self.file.write(str(doc))

    def write(self, path='.'):
        with open(os.path.join(path, self.filename), 'w') as self.file:
            self._write_title()
            self._write_section('classes')
            self._write_section('functions')
            self._write_section('data', level = 4)

class DataDoc:
    def __init__(self, docstring):
        self.doc = docstring
    def __str__(self):
        return '{}\n\n'.format(self.doc)

class ClassDoc:
    def __init__(self, docstring, methods):
        self.doc     = docstring if docstring is not None else ''
        self.methods = methods
    def generatemethods(self):
        return ['##### `{}`\n\n{}'.format(method, doc) for method, doc in self.methods.items() if doc is not None]
    def __str__(self):
        return self.doc + '\n\n' + '#### Methods\n\n' + ''.join([str(doc) + '\n\n' for doc in self.generatemethods()]) + '---\n\n'

if __name__ == "__main__":

    import FoxDot

    docs = GenerateDocs(FoxDot, 'new_docs')
    docs.write()
