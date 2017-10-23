from __future__ import absolute_import, division, print_function

try:
    from Tkinter import Text
except ImportError:
    from tkinter import Text

from .Format import *

try:
    import Queue
except ImportError:
    import queue as Queue

background = colour_map['background']

class ThreadedText(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.config(highlightbackground=background)
        self.height = options.get("height", 20)
        self.queue = Queue.Queue()
        self.update()

    def on_resize(self, event):
        line_h = self.dlineinfo("@0,0")
        if line_h is not None:
            self.height = int((self.winfo_height()-2) / line_h[3])
        return
    
    def update(self):
        """ Recursively called method that monitors as
            queue of Tkinter tasks.
        """
        try:
            
            while True:

                task, args, kwargs = self.queue.get_nowait()

                task(*args, **kwargs)
                
                self.update_idletasks()

        # Break when the queue is empty
        except Queue.Empty:

            pass

        except Exception as e:

            print(e)

        # Recursive call
        self.after(10, self.update)
        return
