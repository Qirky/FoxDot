class Parent:
    pass

class Child(Parent):
    pass

a = Child()

print super(type(a))
