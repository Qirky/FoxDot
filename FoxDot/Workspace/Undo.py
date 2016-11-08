from AppFunctions import index

class UndoStack:
    def __init__(self, tkwidget):
        self.data = []
        self.text = tkwidget
    def append_keystroke(self, i):
        self.data.append(Keystroke(i, self.text))
        return self
    def append_delete(self, text, start, end=None):
        self.data.append(Delete(text, start, end, self.text))
        return self
    def pop(self, i=-1):
        return self.data.pop(i)
    def __len__(self):
        return len(self.data)
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return repr(self.data)

class Keystroke:
    def __init__(self, i, tkwidget):
        self.index = i
        self.text = tkwidget
    def action(self):
        self.text.delete(self.index)
        self.text.mark_set("insert", self.index)
        return

class Delete:
    def __init__(self, text, index1, index2, tkwidget):
        self.string = text
        self.start  = index1
        self.end    = index2
        self.text   = tkwidget

        if self.end is None:
            self.end = self.start
            print index(self.start)
            
    def action(self):
        self.text.insert(self.start, self.string)
        self.text.mark_set("insert", self.end)
        return
        
    
