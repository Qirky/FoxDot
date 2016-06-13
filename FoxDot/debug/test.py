class item:
    def hello(self):
        print "hello"

class test:
    def __init__(self, x):
        self.x = x
    def method(self, func):
        getattr(self, func.__name__).__call__()
    
        

a = test(item())
print a.x

a.method(a.x.hello)



