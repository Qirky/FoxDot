from random import choice
from copy import deepcopy
import Queue
import Grammar

class null:
    def __init__(self, root=True):
        if root:
            self.root=null(False)
    def __repr__(self):
        return "null"
    def after(*args, **kwargs):
        return 0
    def read(self):
        return ""
    def replace(self, *args, **kwargs):
        return
    def exec_line(self, *args, **kwargs):
        return

class Ghost:

    widget = null()

    def __init__(self):

        self.players = {}
        self.index = [0, 0]
        self.instructions = Queue.Queue()
        self.running = True

    def defineInstructions(self, original, syntax):

        new = Grammar.createPlayer(**syntax)

        self.instructions.put((original, new))
        
        return

    def write(self):
        ''' Create a list of instructions '''

        try:

            old, new = self.instructions.get_nowait()

            # 1. Find the line with 'old' on it

            for line, string in enumerate(self.widget.read().split("\n")):

                 if old in string:

                     line += 1

                     break

            else:
                
                 raise Queue.Empty()
                
            # 2. Replace

            self.widget.replace(line, old, new)

            index = str(line) + ".0"

            # 3. Execute

            self.widget.exec_line(event=None, insert=index)

            # Recall

            self.widget.root.after(50, self.write)

        except Queue.Empty:

            if self.running == True:

                self.widget.root.after(choice([2000, 3000, 4000, 5000]), self.act)
            
        return
        

    def getPlayer(self):
        ''' Choose a player from those available '''

        # Read the text from the current widget
        
        text = self.widget.read()

        # Find all the players

        self.players = {}

        for _str, _dict in Grammar.playerData(text):

            # Store dict on the syntax involving a player

            self.players[_str] = _dict

        # Choose whether to create a new one (right now - do not)

        if len(self.players) == 0:

            return None # dict of a new blank player

        else:

            return choice(self.players.keys())

    def act(self):
        ''' main program '''

        p = self.getPlayer()

        if p is not None:

            # Randomly select an action

            action = choice(Grammar.Actions)

            # Get the desired output syntax

            syntax = action(**self.players[p])

            # Work out how to go from p -> new syntax

            self.defineInstructions(p, syntax)

            # Get to the desired outcome

            self.write()

        return

    def stop(self):
        self.running = False

if __name__ == "__main__":
    Ghost(null())
