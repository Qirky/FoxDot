"""

    Draws a fractal graph based on the sound coming out

"""

from random import randint

import Tkinter as Tk

colour = ["red", "blue", "black", "green", "purple", "pink", "yellow"]

class Fractal:
    def __init__(self, w=500, h=500):
        self.root=Tk.Tk()
        self.canvas = Tk.Canvas(self.root, width=w, height=h,
                                background="black")
        self.canvas.pack()
        self.players = []

        self.pad = 10

        self.v_x = [self.pad, w-self.pad, w / 2.0]
        self.v_y = [self.pad, self.pad , h-self.pad]

        self.len = len(self.v_x)

        self.x = [50]
        self.y = [40]

        self.r = 0.5
        

    def __call__(self, player):
        """ Takes information  about the current state of the player
            object and draws a node on the graph """
        # Add new player

        if player.id not in self.players:
            
            self.players.append(player.id)

        p = randint(0, self.len-1)

        x = (self.v_x[-1] * (1-self.r)) + (self.v_x[p] * self.r)
        y = (self.v_y[-1] * (1-self.r)) + (self.v_y[p] * self.r)

        # Draw the x, y

        i = self.players.index(player.id)

        self.draw(x, y, colour[i % len(colour)])

        # Store the co-ordinates

        self.v_x.append(x)
        self.v_y.append(y)

        return

    def draw(self, x, y, fill="black"):

        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=fill, outline=fill)

        return





        
