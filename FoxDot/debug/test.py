class test:
    def __init__(self, val):
        self.v = val
    def __setattr__(self, name, value):
        self.__dict__[name] = value

a = test(10)
print a.v
a.v = 1000
print a.v
