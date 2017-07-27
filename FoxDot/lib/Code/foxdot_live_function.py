""" Allows you continually update a function """

from __future__ import absolute_import, division, print_function

# TODO: dependencies

_live_functions_dict = {}

class _live_function:
    def __init__(self, func, dependency=None):
        self.func = func
        self.name = func.__name__
        self.live = False
        self.dependency = dependency
    def __call__(self, *args, **kwargs):
        self.live = True
        if isinstance(self.dependency,  self.__class__):
            self.dependency.live = False
        return self.func.__call__(*args, **kwargs)
    def update(self, func, dependency=None):
        self.func = func
        if dependency:
            self.dependency = dependency
        return

def livefunction(f, dependency=None):
    """ Wraps a function 'f' in a flexible/interactive way """
    # Live functions can "depend" on others for switching from live or not
    if dependency in _live_functions_dict:
        dependenct = _live_functions_dict[dependency.__name__]
    # Add / update a dictionary of all live functions
    if f.__name__ not in _live_functions_dict:
        _live_functions_dict[f.__name__] = _live_function(f, dependency)
    else:
        _live_functions_dict[f.__name__].update(f, dependency)
    f = _live_functions_dict[f.__name__]
    # If the function is "live" call it
    if f.live: f.__call__()    
    return f


if __name__ == "__main__":
    # debug

    @livefunction
    def part1():
        return 10

    @livefunction
    def part2():
        return 20

    part1()

    print(part1.__class__)
