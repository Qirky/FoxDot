class test:
    def __bool__(self):
        return False


a = test()

print bool(a)
