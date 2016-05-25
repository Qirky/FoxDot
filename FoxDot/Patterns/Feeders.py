"""
    Function in this module take a single Player object as its arguments, changes their state, and return None

    These are to be used in a Player Object's every(n, function) method and create a function that is called every n beats

"""

##from ..Code import LiveObject
##
##class Feeder(LiveObject):
##    def __init__(self, player, metro, step):
##        self.metro = metro
##        self.player = player
##        self.step = step
##        self.__call__()
##    def __call__(self):
##        self.do()
##        LiveObject.__call__(self)
##    def do(self):
##        pass
##
##class rev(Feeder):
##    def do(self):


def rev(player):
    player.reverse()

def lshift(player):
    player.lshift()

def rshift(player):
    player.rshift()

def shuffle(player):

    player.degree = player.degree.shuf()

    try:

        player.pat_to_buf()

    except:

        pass
