from __future__ import absolute_import, print_function

from .VRender import renderizeVoice
from ..SCLang import SampleSynthDef
from ..Buffers import Samples

class VRenderSynthDef(SampleSynthDef):
    def __init__(self):
        SampleSynthDef.__init__(self, "vrender")
        self.pos = self.new_attr_instance("pos")
        self.sample = self.new_attr_instance("sample")
        self.defaults['pos']   = 0
        self.defaults['sample']   = 0
        self.base.append("osc = PlayBuf.ar(2, buf, BufRateScale.kr(buf) * rate, startPos: BufSampleRate.kr(buf) * pos);")
        self.base.append("osc = osc * EnvGen.ar(Env([0,1,1,0],[0.05, sus-0.05, 0.05]));")
        self.osc = self.osc * self.amp
        self.add()

    def __call__(self, filename, pos=0, sample=0, **kwargs):
        lyrics = kwargs['lyrics']
        durations = kwargs['dur']
        notes = kwargs['notes']

        scale = [0,2,4,5,7,9,11]
        if "scale" in kwargs:
            scale = list(kwargs["scale"])

        tempo = 100
        if "tempo" in kwargs:
            tempo = kwargs["tempo"]

        renderizeVoice(filename,lyrics,notes,durations,tempo,scale)

        kwargs = {"dur":sum(kwargs['dur'])}

        kwargs["buf"] = Samples.loadBuffer(filename, sample)
        return SampleSynthDef.__call__(self, pos, **kwargs)

vrender = VRenderSynthDef()
