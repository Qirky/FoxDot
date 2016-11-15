from SCLang import instance, cls

class EnvGen(instance):
    value = "Env"
    doneAction = 2
    def __init__(self, value=None):
        self.value = self.value if value is None else value
    def __str__(self):
        return str( cls("EnvGen").ar(instance(self.__attr__()), doneAction=self.doneAction))
    def __attr__(self):
        """ Converts the attr dict to SCLang arguments """
        args = ",".join(["{}: {}".format(str(key), str(value)) for key, value in self.attr.items()])        
        return self.value + "(" + args + ")"

class env(EnvGen):
    def __init__(self, sus=None, amp=None, curve="'lin'", doneAction=2):
        self.attr={}
        self.attr['times']  = [instance("sus") / 2]*2 if sus is None else sus
        self.attr['levels'] = [0] + ([instance("amp")] if amp is None else amp) + [0]
        self.attr['curve']  = curve
        self.doneAction = doneAction

class perc(EnvGen):
    value = "Env.perc"
    def __init__(self, atk=0.01, sus=None, amp=None, curve=0, doneAction=2):
        self.attr={}
        self.attr['attackTime']  = atk
        self.attr['releaseTime'] = instance("sus") if sus is None else sus
        self.attr['level']       = instance("amp") if amp is None else amp
        self.attr['curve']       = curve
        self.doneAction = doneAction

class linen(perc):
    value = "Env.linen"

class sine(EnvGen):
    value = "Env.sine"
    def __init__(self, dur=instance("sus"), amp=instance("amp"), doneAction=2):
        self.attr={}
        self.attr['dur'] = dur
        self.attr['level'] = amp
        self.doneAction = doneAction

class ramp(EnvGen): # maybe call it ramp?
    def __init__(self, sus=None, amp=[1,1], curve="'step'", doneAction=2):
        self.attr={}
        self.attr['times']  = [instance("sus")] if sus is None else sus
        self.attr['levels'] = [instance("amp") * val for val in amp]
        self.attr['curve']  = curve
        self.doneAction = doneAction

class reverse(EnvGen):
    def __init__(self, sus=None, amp=None, curve="'exp'", doneAction=2):
        self.attr={}
        self.attr['times']  = [instance("sus") if sus is None else sus, 0.001]
        self.attr['levels'] = [0] + [instance("amp")] if amp is None else amp + [0]
        self.attr['curve']  = curve
        self.doneAction = doneAction

amp = instance("amp")
sus = instance("sus")
