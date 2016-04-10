class dad:

    def __init__(self, x):
        self.x = x
        self.y = -1 if self.x > 10 else 1

a = dad(11)
print a.x, a.y

b = dad(9)
print b.x, b.y
