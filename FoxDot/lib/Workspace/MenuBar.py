from __future__ import absolute_import, division, print_function

from .tkimport import Menu, BooleanVar, IntVar, DISABLED

import os.path
from functools import partial
from ..Settings import *
from ..Code import FoxDotCode

# Code menu

ctrl = "Command" if SYSTEM == MAC_OS else "Ctrl"

class MenuBar(Menu):
    def __init__(self, master, visible=True):

        self.root = master

        Menu.__init__(self, master.root)

        # "ticked" menu options

        self.sc3_plugins = BooleanVar()
        self.sc3_plugins.set(SC3_PLUGINS)

        self.cpu_usage = IntVar()
        self.cpu_usage.set(CPU_USAGE)

        self.latency = IntVar()
        self.latency.set(CLOCK_LATENCY)

        # File menu

        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label="New Document",  command=self.root.newfile,  accelerator="Ctrl+N")
        filemenu.add_command(label="Open",          command=self.root.openfile, accelerator="Ctrl+O")
        filemenu.add_command(label="Save",          command=self.root.save,     accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...",    command=self.root.saveAs )
        self.add_cascade(label="File", menu=filemenu)

        # Edit menu

        editmenu = Menu(self, tearoff=0)
        editmenu.add_command(label="Undo",        command=self.root.undo, accelerator="Ctrl+Z")
        editmenu.add_command(label="Redo",        command=self.root.redo, accelerator="Ctrl+Y")
        editmenu.add_separator()
        editmenu.add_command(label="Cut",        command=self.root.edit_cut,   accelerator="Ctrl+X")
        editmenu.add_command(label="Copy",       command=self.root.edit_copy,  accelerator="Ctrl+C")
        editmenu.add_command(label="Paste",      command=self.root.edit_paste, accelerator="Ctrl+V")
        editmenu.add_command(label="Select All", command=self.root.select_all,  accelerator="Ctrl+A")
        editmenu.add_separator()
        editmenu.add_command(label="Increase Font Size",      command=self.root.zoom_in, accelerator="Ctrl+=")
        editmenu.add_command(label="Decrease Font Size",      command=self.root.zoom_out, accelerator="Ctrl+-")
        editmenu.add_separator()
        editmenu.add_command(label="Clear Console",          command=self.root.clear_console)
        editmenu.add_command(label="Export Console Log",     command=self.root.export_console)
        editmenu.add_command(label="Toggle Console",         command=self.root.toggle_console)
        editmenu.add_separator()
        editmenu.add_checkbutton(label="Toggle Fullscreen",      command=(lambda: self.root.toggle_true_fullscreen(zoom=True)), variable=self.root.true_fullscreen_toggled)
        editmenu.add_command(label="Toggle Menu",            command=self.root.toggle_menu, accelerator="Ctrl+M")
        editmenu.add_checkbutton(label="Toggle Window Transparency",  command=self.root.toggle_transparency, variable=self.root.transparent)
        editmenu.add_checkbutton(label="Toggle Auto-fill Prompt",     command=self.root.toggle_prompt,       variable=self.root.show_prompt)
        self.add_cascade(label="Edit", menu=editmenu)
        
        # Note: Alt renders properly to look like Option, so we don't need a
        # conditional for those shortcuts

        codemenu = Menu(self, tearoff=0)
        codemenu.add_command(label="Evaluate Block",         command=self.root.exec_block,  accelerator="{}+Return".format(ctrl))
        codemenu.add_command(label="Evaluate Line",          command=self.root.exec_line,   accelerator="Alt+Return")
        codemenu.add_command(label="Clear Scheduling Clock", command=self.root.killall,     accelerator="{}+.".format(ctrl))
        codemenu.add_separator()
        codemenu.add_checkbutton(label="Use SC3 Plugins",    command=self.root.toggle_sc3_plugins, variable=self.sc3_plugins)
        codemenu.add_separator()
        codemenu.add_checkbutton(label="Listen for connections", command=self.root.allow_connections, variable=self.root.listening_for_connections)
        self.add_cascade(label="Language", menu=codemenu)


        # Help

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label="Display help message", comman=self.root.help, accelerator="{}+{}".format(ctrl, self.root.help_key))
        helpmenu.add_command(label="Visit FoxDot Homepage", command=self.root.openhomepage)
        helpmenu.add_command(label="Documentation",   command=self.root.opendocumentation)
        helpmenu.add_separator()
        cpu_menu=Menu(self, tearoff=0)
        cpu_menu.add_radiobutton(label="Low", variable=self.cpu_usage, value=0, command=self.set_cpu_usage)
        cpu_menu.add_radiobutton(label="Medium", variable=self.cpu_usage, value=1, command=self.set_cpu_usage)
        cpu_menu.add_radiobutton(label="High", variable=self.cpu_usage, value=2, command=self.set_cpu_usage)
        helpmenu.add_cascade(label="CPU Usage", menu=cpu_menu)
        lat_menu=Menu(self, tearoff=0)
        lat_menu.add_radiobutton(label="Low", variable=self.latency, value=0, command=self.set_latency)
        lat_menu.add_radiobutton(label="Medium", variable=self.latency, value=1, command=self.set_latency)
        lat_menu.add_radiobutton(label="High", variable=self.latency, value=2, command=self.set_latency)
        helpmenu.add_cascade(label="Clock Latency", menu=lat_menu)
        helpmenu.add_separator()
        helpmenu.add_command(label="Open Samples Folder",   command=self.root.open_samples_folder)
        helpmenu.add_command(label="Open config file (advanced)",      command=self.root.open_config_file)
        self.add_cascade(label="Help & Settings", menu=helpmenu)

        # Tutorials

        tutorialmenu = Menu(self, tearoff=0)

        for tutorial in GET_TUTORIAL_FILES():

            filename = os.path.basename(tutorial)

            if filename.endswith(".py"):

                filename = filename.replace(".py", "")

                data = filename.split("_")

                num  = data[0]
                name = " ".join(data[1:]).title()

                tutorialmenu.add_command(label="Load Tutorial {}: {}".format(num, name), command=partial(self.root.loadfile, tutorial))

        self.add_cascade(label="Tutorials", menu=tutorialmenu)

        # Add to root

        self.visible = visible
        
        if self.visible:
            
            master.root.config(menu=self)

    def toggle(self):
        """ Hides/shows this menu """
        self.root.root.config(menu=self if not self.visible else 0)
        self.visible = not self.visible
        return

    def allow_connections(self, **kwargs):
        """ Starts a new instance of ServerManager.TempoServer and connects it with the clock """
        if self.listening_for_connections.get() == True:
            Clock = self.root.namespace["Clock"]
            Clock.start_tempo_server(TempoServer, **kwargs)
            print("Listening for connections on {}".format(Clock.tempo_server))
        else:
            Clock = self.root.namespace["Clock"]
            Clock.kill_tempo_server()
            print("Closed connections")
        return

    def start_listening(self, **kwargs):
        """ Manual starting of FoxDot tempo server """
        # TODO - take this method out of the menu
        self.listening_for_connections.set(not self.listening_for_connections.get())
        self.allow_connections(**kwargs)
        return

    def set_cpu_usage(self, *args):
        """ Updates the cpu usage option """
        self.root.namespace["Clock"].set_cpu_usage(self.cpu_usage.get())
        return

    def set_latency(self, *args):
        """ Updates the cpu usage option """
        self.root.namespace["Clock"].set_latency(self.latency.get())
        return


class PopupMenu(Menu):
    def __init__(self, master, **kwargs):
        self.root = master
        Menu.__init__(self, master.root, tearoff=0)
        self.add_command(label="Undo", command=self.root.undo, accelerator="{}+Z".format(ctrl)) 
        self.add_command(label="Redo", command=self.root.redo, accelerator="{}+Y".format(ctrl))
        self.add_separator()
        self.add_command(label="Copy", command=self.root.edit_copy, accelerator="{}+C".format(ctrl))
        self.add_command(label="Cut", command=self.root.edit_cut, accelerator="{}+X".format(ctrl))
        self.add_command(label="Paste", command=self.root.edit_paste, accelerator="{}+V".format(ctrl))
        self.add_separator()
        self.add_command(label="Select All", command=self.root.select_all, accelerator="{}+A".format(ctrl))
        self.bind("<FocusOut>", self.hide) # hide when clicked off


    def show(self, event):
        """ Displays the popup menu """
        try:
            self.post(event.x_root, event.y_root)
        finally:
            self.grab_release()

    def hide(self, event):
        """ Removes menu from sight """
        self.unpost()


class ConsolePopupMenu(Menu):
    def __init__(self, master, **kwargs):
        self.root = master
        Menu.__init__(self, master.root, tearoff=0)
        self.add_command(label="Undo", state=DISABLED, accelerator="{}+Z".format(ctrl))
        self.add_command(label="Redo", state=DISABLED, accelerator="{}+Y".format(ctrl))
        self.add_separator()
        self.add_command(label="Copy", command=self.root.edit_copy, accelerator="{}+C".format(ctrl))
        self.add_command(label="Cut", state=DISABLED, accelerator="{}+X".format(ctrl))
        self.add_command(label="Paste", state=DISABLED, accelerator="{}+V".format(ctrl))
        self.add_separator()
        self.add_command(label="Select All", command=self.root.select_all, accelerator="{}+A".format(ctrl))
        self.bind("<FocusOut>", self.hide) # hide when clicked off

    def show(self, event):
        """ Displays the popup menu """
        try:
            self.post(event.x_root, event.y_root)
        finally:
            self.grab_release()

    def hide(self, event):
        """ Removes menu from sight """
        self.unpost()
        
