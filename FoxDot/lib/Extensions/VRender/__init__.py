from __future__ import absolute_import, print_function

from .VRender import renderizeVoice
from ...SCLang import SynthDef
from ... import Clock, Scale, Root
from ...Settings import FOXDOT_ROOT

class VRenderSynthDef(SynthDef):
    def __init__(self):
        SynthDef.__init__(self, "vrender")
        self.add()

    def __call__(self, notes, pos=0, sample=0, **kwargs):

        if "lyrics" in kwargs:
            lyrics = kwargs['lyrics']
        else:
            lyrics = "oo "

        if "dur" in kwargs:
            durations = kwargs['dur']
        else:
            durations = [1]

        if 'file' in kwargs:
            filename = kwargs['file']
        else:
            filename = 'v1'

        if "sex" in kwargs:
            sex = kwargs["sex"]
        else:
            sex = "female"

        scale = list(Scale.default)
        tempo = int(Clock.bpm)

        notes = list(map(lambda x: x + Root.default,notes))

        renderizeVoice(filename,lyrics,notes,durations,tempo,scale,sex,FOXDOT_ROOT)

vrender = VRenderSynthDef()