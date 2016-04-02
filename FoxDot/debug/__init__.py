def show(func):
    def func_wrapper(x, y):
        return func(x, y) * 2
    return func_wrapper

@show
def add(a,b):
    return a + b

print add(2,4)

