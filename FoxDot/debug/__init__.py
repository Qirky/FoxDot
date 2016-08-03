class A:
    def __init__(self, x):
        self.x=x
    def method1(self):
        print self.x
    def method2(self):
        print "2222222222222222"

class B:
    def __init__(self, action):
        self.method=action
    def action(self):
        self.method.__call__()

test = A(100)

item = B(test.method1)

item.action()
