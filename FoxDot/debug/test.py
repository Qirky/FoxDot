class foo:
    value = "foo"

class bar:
    value = "bar"
    def change(self):
        self.__class__ = foo

a = bar()

print a.value

a.change()

print a.value
