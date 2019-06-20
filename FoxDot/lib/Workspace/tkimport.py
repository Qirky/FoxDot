import sys

if sys.version_info[0] >= 3:
    from tkinter import *
    from tkinter import ttk
    from tkinter import font as tkFont
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox
else:
    from Tkinter import *
    import ttk
    import tkFont
    import tkFileDialog
    import tkMessageBox