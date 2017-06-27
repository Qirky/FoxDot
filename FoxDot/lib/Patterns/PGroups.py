from Main import Pattern, PGroup, PGroupPrime, PGroupStar

class PGroupPlus(PGroupPrime):
    """ Stutters the values over the length of and event's 'sus' """
    bracket_style="+()"
    def get_behaviour(self):
        def action(event, key):
            event['delay'] += self.calculate_time(float(event['sus']))
            return event
        return action

class PGroupPow(PGroupPrime):
    """ Stutters a shuffled version the values over the length of and event's 'dur' """
    bracket_style="**()"
    def calculate_time(self, dur):
        return PGroupPrime.calculate_time(self, dur).shuffle()    

class PGroupDiv(PGroupPrime):
    """ Stutter every other request """
    bracket_style="/()"
    counter = 0
    def __init__(self, *args, **kwargs):
        PGroupPrime.__init__(self, *args, **kwargs)
    def change_state(self):
        self.counter += 1
    def calculate_time(self, dur):
        if self.counter % 2 == 1:
            return PGroupPrime.calculate_time(self, dur)
        else:
            return 0

class PGroupFloorDiv(PGroupPrime):
    """ Unused """
    bracket_style="//()"

class PGroupMod(PGroupPrime):
    """ Unused """
    bracket_style="%()"

class PGroupSub(PGroupPrime):
    """ Unused """
    bracket_style="-()"

class PGroupXor(PGroupPrime):
    """ Unused """
    bracket_style="^()"

class PGroupAnd(PGroupPrime):
    """ Unused """
    bracket_style="&()"
    delay = 0
    def __init__(self, args):
        PGroupPrime.__init__(self, args[0])
        if len(args) > 0:
            self.delay = args[1]
    def calculate_step(self, i, dur):
        return i * self.delay

class PGroupOr(PGroupPrime):
    """ Unused """
    bracket_style="|()"

# Here we can define methods for Pattern that return Patterns of PGroups
    

