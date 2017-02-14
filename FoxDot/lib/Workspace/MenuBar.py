from Tkinter import Menu

class MenuBar(Menu):
    def __init__(self, master, visible=True):

        self.root = master

        Menu.__init__(self, master.root)

        # Set font
        
        self.config(font="CodeFont")

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
        editmenu.add_command(label="Select All", command=self.root.selectall,  accelerator="Ctrl+A")
        editmenu.add_separator()
        editmenu.add_command(label="Increase Font Size",      command=self.root.zoom_in, accelerator="Ctrl+=")
        editmenu.add_command(label="Decrease Font Size",      command=self.root.zoom_out, accelerator="Ctrl+-")
        editmenu.add_separator()
        editmenu.add_command(label="Toggle Menu", command=self.root.toggle_menu, accelerator="Ctrl+M")
        self.add_cascade(label="Edit", menu=editmenu)

        # Code menu

        codemenu = Menu(self, tearoff=0)
        codemenu.add_command(label="Evaluate Block",         command=self.root.exec_block,  accelerator="Ctrl+Return")
        codemenu.add_command(label="Evaluate Line",          command=self.root.exec_line,   accelerator="Alt+Return")
        codemenu.add_command(label="Clear Scheduling Clock", command=self.root.killall,     accelerator="Ctrl+.")
        codemenu.add_command(label="Toggle Console",         command=self.root.toggle_console)
        self.add_cascade(label="Code", menu=codemenu)

        # Settings

##        settingsmenu = Menu(self, tearoff=0)
##        settingsmenu.add_command(label="Preferences...",      command=self.root.toggleMenu)
##        settingsmenu.add_command(label="Change Colours...",   command=self.root.toggleMenu)
##        settingsmenu.add_command(label="Open Samples Folder", command=self.root.toggleMenu)
##        self.add_cascade(label="Settings", menu=settingsmenu)

        # Help

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label="Visit FoxDot Homepage", command=self.root.openhomepage)
        helpmenu.add_command(label="Documentation",   command=self.root.opendocumentation)
        self.add_cascade(label="Help", menu=helpmenu)

        # Add to root

        self.visible = visible
        
        if self.visible:
            
            master.root.config(menu=self)

    def toggle(self):
        self.root.root.config(menu=self if not self.visible else 0)
        self.visible = not self.visible
        return
