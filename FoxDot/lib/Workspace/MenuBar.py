from Tkinter import Menu

class MenuBar(Menu):
    def __init__(self, master, visible=True):

        self.root = master

        Menu.__init__(self, master.root)

        # Set font
        
        self.config(font="CodeFont")

        # File menu

        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label="New Document",  command=self.root.openfile, accelerator="Ctrl+N")
        filemenu.add_command(label="Open",          command=self.root.openfile, accelerator="Ctrl+O")
        filemenu.add_command(label="Save",          command=self.root.save,     accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...",    command=self.root.save,     accelerator="Ctrl+Shift+S")
        self.add_cascade(label="File", menu=filemenu)

        # Edit menu

        editmenu = Menu(self, tearoff=0)
        editmenu.add_command(label="Undo",        command=self.root.undo, accelerator="Ctrl+Z")
        editmenu.add_command(label="Redo",        command=self.root.redo, accelerator="Ctrl+Y")
        editmenu.add_separator()
        editmenu.add_command(label="Cut",        command=self.root.toggleMenu, accelerator="Ctrl+X")
        editmenu.add_command(label="Copy",       command=self.root.toggleMenu, accelerator="Ctrl+C")
        editmenu.add_command(label="Paste",      command=self.root.paste,      accelerator="Ctrl+V")
        editmenu.add_command(label="Select All", command=self.root.toggleMenu, accelerator="Ctrl+A")
        editmenu.add_separator()
        editmenu.add_command(label="Increase Font Size",      command=self.root.zoom_in, accelerator="Ctrl+=")
        editmenu.add_command(label="Decrease Font Size",      command=self.root.zoom_out, accelerator="Ctrl+-")
        editmenu.add_separator()
        editmenu.add_command(label="Toggle Menu", command=self.root.toggleMenu, accelerator="Ctrl+M")
        self.add_cascade(label="Edit", menu=editmenu)

        # Code menu

        codemenu = Menu(self, tearoff=0)
        codemenu.add_command(label="Evaluate Block",         command=self.root.exec_block,  accelerator="Ctrl+Return")
        codemenu.add_command(label="Evaluate Line",          command=self.root.exec_line,   accelerator="Alt+Return")
        codemenu.add_command(label="Clear Scheduling Clock", command=self.root.killall,     accelerator="Ctrl+.")
        codemenu.add_command(label="Clear Console",          command=self.root.killall,     accelerator="Ctrl+Shift+C")
        self.add_cascade(label="Code", menu=codemenu)

        # Settings

        settingsmenu = Menu(self, tearoff=0)
        settingsmenu.add_command(label="Preferences...", command=self.root.toggleMenu)
        settingsmenu.add_command(label="Change Colours...", command=self.root.toggleMenu)
        self.add_cascade(label="Settings", menu=settingsmenu)

        # Help

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label="FoxDot Homepage", command=self.root.openhomepage)
        helpmenu.add_command(label="Documentation", command=self.root.opendocumentation)
        self.add_cascade(label="Help", menu=helpmenu)

        # Add to root
        if visible:
            master.root.config(menu=self)
