import inspect
import signal
import re
from dataclasses import dataclass
from collections import deque
from contextlib import suppress

from .tkimport import *
from .AppFunctions import index as get_index
from .Format import get_keywords
from ..Effects import FxList
from ..TimeVar import var

try:
    import jedi
    enable_jedi_complete = True

    jedi.settings.auto_import_modules = [
        "gi",
        "FoxDot",
        "FoxDot.lib",
        "FoxDot.lib.Code",
        "FoxDot.lib.Custom",
        "FoxDot.lib.Extensions",
        "FoxDot.lib.Extensions.VRender",
        "FoxDot.lib.Extensions.SonicPi",
        "FoxDot.lib.Workspace",
        "FoxDot.lib.Workspace.Simple",
        "FoxDot.lib.EspGrid",
        "FoxDot.lib.Effects",
        "FoxDot.lib.Patterns",
        "FoxDot.lib.SCLang",
        "FoxDot.lib.Settings",
        "FoxDot.lib.Utils",
    ]
except (ModuleNotFoundError, ImportError):
    jedi = None
    enable_jedi_complete = False


def replace_player_signature(p: 'type[Player]'):
    signature = inspect.signature(p)
    parameters = []

    params = list(p.fx_attributes)
    for key in p.fx_attributes:
        default = FxList.defaults[key]
        parameters.append(
            inspect.Parameter(
                name=key,
                default=default,
                kind=inspect.Parameter.KEYWORD_ONLY,
            ),
        )

    for attr in filter(
        lambda x: x not in params,
        set(p.keywords + p.envelope_keywords + p.base_attributes),
    ):
        parameters.append(
            inspect.Parameter(
                name=attr,
                kind=inspect.Parameter.KEYWORD_ONLY,
            ),
        )

    p.__signature__ = signature.replace(parameters=parameters)
    return p


@dataclass
class FoxDotComplete:
    name: str
    type: str = 'FoxDot'

    def docstring(self):
        return ''


class Timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


class TextPrompt:
    enable_jedi_complete = enable_jedi_complete  # GUI.prompt.enable_jedi_complete = False
    timeout = 5  # GUI.prompt.timeout_complete = .5
    tab_complete = True  # GUI.prompt.tab_complete = False
    show_docstring = False  # GUI.prompt.show_docstring = True

    visible = True
    docstring_visible = False

    selected = 0
    num_items = 6
    pady = 2

    def __init__(self, root):
        self.root = root
        self.master = self.root.text # text box

        self.values = [StringVar() for n in range(self.num_items)]
        self.clear()

        self.labels = [Label(self.master, textvariable=self.values[n], font=self.root.codefont, foreground="White", anchor=NW, pady=self.pady) for n in range(self.num_items)]

        self.selected = 0
        self.bg = "gray40"
        self.fg = "gray30"

        self.suggestions = deque()

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

        self.re = re.compile(r"(\w+)$")

        self.__visible = True
        self.anchor = None

        self.hide()

        # Binds
        self.master.bind('<Tab>', lambda event: self.tab())
        self.master.bind('<Escape>', lambda event: self.escape())
        self.master.bind('<Control-space>', lambda event: self.toogle(force=True))
        self.master.bind('<Control-D>', lambda event: self.toggle_docstring())

        # Docstring
        self.docstring_visible = False
        self.docstring_var = StringVar()
        self.docstring = Label(
            self.master,
            textvariable=self.docstring_var,
            font=self.root.codefont,
            foreground='White',
            anchor=W,
            justify='left',
            pady=self.pady,
        )

    @property
    def namespace(self):
        _namespace = set(self.root.namespace)
        _namespace |= set(get_keywords())
        _namespace |= set(self.root.namespace["SynthDefs"])
        _namespace |= set(self.root.namespace["Player"].get_attributes())
        _namespace |= {"every", "often", "sometimes", "rarely"}
        _namespace |= set(self.root.namespace["Pattern"].get_methods())
        _namespace |= set(self.root.namespace["Scale"].names())
        _namespace |= {"SynthDefs"}
        return sorted(list(_namespace))

    def get_start_of_word(self):
        """ Returns the TK index and characters directly preceeding the INSERT marker """
        # Get contents of this line up to the INSERT
        row, col = get_index(self.master.index(INSERT))
        start, end = f"{row}.0", f"{row}.{col}"
        text = self.master.get(start, end)
        match = self.re.search(text)

        if match is not None:
            index, text = f"{row}.{match.start()}", match.group(0)
            self.anchor = match.span()
        else:
            index, text = "1.0", ""
            self.anchor = None

        return (index, text)

    def in_word(self):
        """ Returns True if the next character is alphanumeric """
        return self.master.get(INSERT).isalnum()

    def clear(self):
        for value in self.values:
            value.set("")

    def tab(self):
        """Tab complete action."""
        if not self.visible or not self.tab_complete:
            return self.root.tab()
        self.autocomplete()
        return 'break'

    def escape(self):
        """Hide prompt if visible."""
        if not self.visible:
            return self.root.toggle_true_fullscreen()
        self.hide()

        if self.docstring_visible:
            self.toggle_docstring()

        return 'break'

    def toogle(self, force=False):
        """Toggle prompt"""
        self.hide() if self.visible else self.show(force=force)
        return 'break'

    def update_docstring(self, helpers):
        if not helpers or not (doc := helpers[0].docstring()):
            return

        self.docstring_var.set(doc)

        width = max(len(line) for line in self.docstring_var.get().splitlines())
        self.docstring.config(width=width, bg=self.fg)

        x = self.x if self.x < 9999 else 200
        y = self.y if self.y < 9999 else 20

        length  = max((len(val.get()) for val in self.values))
        base = length * 20 if length else 300

        self.docstring.place(x=x+base, y=y+42)
        self.docstring_visible = True

    def toggle_docstring(self, helpers=None):
        self.docstring_var.set('')

        if not self.docstring_visible:
            line, column = get_index(self.master.index(INSERT))
            try:
                return self.update_docstring(helpers or self.interpreter.help(line, column))
            except AttributeError:
                print('AttributeError')

        self.docstring.place(x=9999, y=9999)
        self.docstring_visible = False

    def hide(self):
        self.clear()
        self.move(x=9999, y=9999)
        self.visible = False

        if self.docstring_visible:
            self.toggle_docstring()

    def show(self, force=False):
        """Displays the prompt with suggestions."""
        _, column = get_index(self.master.index(INSERT))
        if column == 0 and not force:
            return

        if not (bbox := self.master.bbox(INSERT)):
            return

        self.selected = 0
        self.x, self.y, self.w, self.h = bbox

        _, word = self.get_start_of_word()

        suggestions = self.find_suggestions()
        if not suggestions and word:
            names = [s.name for s in suggestions]
            for name in self.namespace:
                if name.startswith(word) and name not in names:
                    suggestions.append(FoxDotComplete(name=name))
        self.suggestions = deque(suggestions)

        if not self.suggestions or word == self.suggestions[0]:
            return self.hide()

        self.update_values()
        self.move(self.x, self.y)
        self.visible = True

    def update_values(self):
        """Update values."""
        total = len(self.suggestions)
        for row, value in enumerate(self.values):
            if row >= total:
                value.set('')
                continue

            value.set(self.suggestions[row].name)
            if self.show_docstring and row == self.selected:
                self.docstring_visible = False
                self.toggle_docstring([self.suggestions[row]])

    @property
    def interpreter(self):
        namespace = self.root.namespace.copy()
        # adicionando attributes e fxList aos kwargs
        player_class = replace_player_signature(namespace['Player'])
        # mentindo que SynthDefProxy é Player
        for name in list(namespace['SynthDefs']) + ['play']:
            namespace[name] = player_class

        return jedi.Interpreter(
            self.master.get('1.0', END),
            [namespace],
            path=self.root.filename,
            project=jedi.Project(self.root.namespace['Settings'].USER_CWD),
        )

    def find_suggestions(self, fuzzy=False):
        line, column = get_index(self.master.index(INSERT))
        if self.enable_jedi_complete and jedi:
            with suppress(TimeoutError), Timeout(seconds=self.timeout):
                return self.interpreter.complete(line, column, fuzzy=fuzzy)
        return []


    def move(self, x, y):
        offset = self.h
        width  = max((len(val.get()) for val in self.values))
        for i, label in enumerate(self.labels):
            if self.values[i].get() == "":
                label.place(x=9999, y=9999)
                continue

            label.place(x=x, y=y + offset)
            label.config(width=width, bg=(self.fg if self.selected == i else self.bg),)
            offset += (self.h + (self.pady * 2))
            if self.selected == i and self.show_docstring:
                self.docstring_visible = False
                self.toggle_docstring([self.suggestions[i]])

    def cycle_up(self):
        if self.selected == 0:
            self.suggestions.rotate()
            self.update_values()
        self.selected = max(0, self.selected - 1)
        self.update_values()
        return self.move(self.x, self.y)

    def cycle_down(self):
        selected = self.selected + 1
        if selected >= self.num_items:
            self.suggestions.rotate(-1)
            self.update_values()
        last_row = min(len(self.suggestions), self.num_items)
        self.selected = min(last_row - 1, selected)
        self.update_values()
        return self.move(self.x, self.y)

    def autocomplete(self):
        """ Inserts the remainder of the currently highlited suggestion """
        if self.anchor is not None:
            LENGTH = self.anchor[1] - self.anchor[0]
            self.master.delete(f"{INSERT}-{LENGTH}c", INSERT)
            WORD  = self.values[self.selected].get()
            self.master.insert(INSERT, WORD)
            self.root.update()
        self.hide()
