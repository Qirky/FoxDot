class test(object):
    def __init__(self):
        self.x = 10
        self.y = 20
    def __getattr__(self, key):
        print key
        return 99
    def __getattribute__(self, key):
        try:
            object.__getattribute__(self, key)
        except:
            return 999

a = test()

print a.x

print a.z
