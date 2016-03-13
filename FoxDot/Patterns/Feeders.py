"""
    Function in this module take a single Player object as its arguments, changes their state, and return None

    These are to be used in a Player Object's every(n, function) method and create a function that is called every n beats

"""

def rev(player):
    player.reverse()

def lshift(player):
    player.lshift()

def rshift(player):
    player.rshift()

def shuf(player):
    player.degree = Shuf(player.degree)
