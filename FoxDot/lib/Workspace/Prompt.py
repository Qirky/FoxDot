from __future__ import absolute_import, division, print_function

from .tkimport import *

from ..Settings import FONT
from .AppFunctions import index as get_index
from .Format import get_keywords
import re

class TextPrompt:
    num_items = 6
    pady = 2
    def __init__(self, root):
        self.root = root
        self.master = self.root.text # text box

        # TODO // sort out the name space to check for suggestions

        # keywords = list(self.root.namespace["get_keywords"]())
        keywords = list(get_keywords())
        synthdefs = list(self.root.namespace["SynthDefs"])
        attributes = list(self.root.namespace["Player"].get_attributes())
        player_methods = ["every", "often", "sometimes", "rarely"]
        pattern_methods = list(self.root.namespace["Pattern"].get_methods())
        scales = list(self.root.namespace["Scale"].names())
        other = ["SynthDefs"]

        self.namespace = sorted(list(set(keywords + synthdefs + attributes + player_methods + pattern_methods + scales + other)))

        self.values = [StringVar() for n in range(self.num_items)]
        self.clear()

        self.labels = [Label(self.master, textvariable=self.values[n], font=self.root.codefont, foreground="White", anchor=NW, pady=self.pady) for n in range(self.num_items)]

        self.selected = 0
        self.bg = "gray40"
        self.fg = "gray30"

        self.suggestions = []

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

        self.re = re.compile(r"(\w+)$")

        self.__visible = True

        self.hide()

    def get_start_of_word(self):
        """ Returns the TK index and characters directly preceeding the INSERT marker """
        # Get contents of this line up to the INSERT

        row, col = get_index(self.master.index(INSERT))

        start, end = "{}.0".format(row), "{}.{}".format(row, col)

        text = self.master.get(start, end)

        match = self.re.search(text)

        if match is not None:

            index, text = "{}.{}".format(row, match.start()), match.group(0)

            self.anchor = match.span()

        else:

            index, text = "1.0", ""

            self.anchor = None

        return (index, text)

    def in_word(self):
        """ Returns True if the next character is alphanumeric """
        return self.master.get(INSERT).isalnum()

    def show(self):
        """ Displays the prompt with suggestions """

        if not self.__visible:

            return

        # 1. Get location - start of the word

        index, word = self.get_start_of_word()

        # If there is a alphanumeric character next, dont show

        if len(word) == 0 or self.in_word():

            return self.hide()

        bbox = self.master.bbox(index)

        if bbox is not None:

            self.selected = 0

            self.x, self.y, self.w, self.h = bbox

            # 3. Find first 4 words

            self.suggestions = self.find_suggestions(word)

            # If there is only 1 suggestion and we're at the end of the word (or no suggestions), just hide

            num_suggestions = len(self.suggestions)

            if num_suggestions == 0 or (num_suggestions == 1 and (word == self.suggestions[0])):

                return self.hide()

            # 4. Show

            self.update_values(self.suggestions)

            self.move(self.x, self.y)

            self.visible = True

        return

    def move(self, x, y):
        offset = self.h
        width  = max((len(val.get()) for val in self.values))
        for i, label in enumerate(self.labels):
            if self.values[i].get() != "":
                label.place(x=x, y=y + offset)
                label.config(width=width, bg=(self.fg if self.selected == i else self.bg),)
                offset += (self.h + (self.pady * 2))
            else:
                label.place(x=9999, y=9999)
        return

    def hide(self):
        self.clear()
        self.move(x=9999, y=9999)
        self.visible = False
        return

    def clear(self):
        for value in self.values:
            value.set("")
        return

    def update_values(self, values):
        self.clear()
        for i, word in enumerate(values[:self.num_items]):
            self.values[i].set(word)
        return

    def find_suggestions(self, word):
        words = []
        i = 0
        for phrase in self.namespace:
            # if phrase.lower().startswith(word.lower()):
            if phrase.startswith(word):
                words.append(phrase)
                i += 1
            if i == self.num_items:
                break
        return words

    def cycle_up(self):
        self.selected = max(0, self.selected - 1)
        return self.move(self.x, self.y)

    def cycle_down(self):
        self.selected = min(len(self.suggestions) - 1, self.selected + 1)
        return self.move(self.x, self.y)

    def autocomplete(self):
        """ Inserts the remainder of the currently highlited suggestion """
        if self.anchor is not None:
            LENGTH = self.anchor[1] - self.anchor[0]
            self.master.delete("{}-{}c".format(INSERT, LENGTH), INSERT)
            WORD  = self.values[self.selected].get()
            self.master.insert(INSERT, WORD)
            self.root.update()
        self.hide()
        return

    def toggle(self):
        """ Flags the prompt to show / not show automatically """
        self.__visible = not self.__visible
        return
