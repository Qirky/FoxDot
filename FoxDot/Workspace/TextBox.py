from Tkinter import Text
from Format import *
import Queue

background = colour_map['background']

class ThreadedText(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = Queue.Queue()
        self.update()
    
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

        # Recursive call
        self.after(10, self.update)
        return
