class test:
    def __init__(self):
        self.x = 10
    def increase(self, x):
        self.x += x
    def do(self, cmd, *args):
        self.cmd(args)

increase = test.increase

a = test()
a.do(increase, 10)
print a.x




        
