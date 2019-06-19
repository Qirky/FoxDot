# Try accessibility version

try:
    import Tka11y as Tkinter
except ImportError:
    pass

try:
    from Tkinter import *
    import ttk
    import tkFont
    import tkFileDialog
    import tkMessageBox
except ImportError:
    from tkinter import *
    from tkinter import ttk
    from tkinter import font as tkFont
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox