class test:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.values = lambda: self.x*self.y


a = test(10,20)

print a.values()

a.x = 2
a.y = 5

print a.values()
