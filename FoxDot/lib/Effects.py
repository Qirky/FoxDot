### Dict of Player keywords to Effects name
##FxAttr = {
##    'chop': 'chop',
##    'bits': 'bitcrush',
##    'verb': 'reverb',
##    'room': 'reverb',
##    'hpf' : 'hpf',
##    'lpf' : 'lpf',
##    'echo': 'echo'
##    }
##
##FxList = {
##    'chop'     : ['chop', 'sus'],
##    'bitcrush' : ['bits'],
##    'reverb'   : ['verb', 'room'],
##    'hpf'      : ['hpf'],
##    'lpf'      : ['lpf'],
##    'echo'     : ['echo']
##    }

FxList = {}

class _count:
    def __init__(self, x):
        self.x=x
    def next(self):
        self.x+=1
        return self.x
    
counter = _count(1001)

class Effect:
    def __init__(self, foxdot_name, sc_name, args):
        self.name      = foxdot_name
        self.node_name = sc_name
        self.args      = args
        self.node_id   = counter.next()
        FxList[self.name] = self
    def __repr__(self):
        return "<Fx '{}'>".format(self.node_name)

Effect('chop','chop', ['chop','sus'])
Effect('bits','bitcrush', ['bits'])
Effect('verb','reverb',['chop', 'room'])
Effect('hpf','hpf',['hpf'])
Effect('lpf','lpf',['lpf'])
Effect('echo', 'echo', ['echo','sus'])    
