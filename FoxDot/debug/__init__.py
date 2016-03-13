class test:

    def __init__(self, val):
        self.x = val
    def val(self):
        return self.x

a = test(10)
b = test(20)
c = test(5)

print min(a,b,c, key=lambda x:x.val()).val()
