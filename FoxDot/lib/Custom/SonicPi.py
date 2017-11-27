from __future__ import print_function

import os

import json
from subprocess import check_output

from ..Midi import freqtomidi
from ..SCLang import CompiledSynthDef


class SonicPiSynthDef(CompiledSynthDef):
    bus_name = 'out_bus'

    def __init__(self, name, filename, synthdata):
        super(SonicPiSynthDef, self).__init__(name, filename)
        self._arg_defaults = synthdata['arg_defaults']
        for key in self._arg_defaults:
            if not hasattr(self, key):
                setattr(self, key, self.new_attr_instance(key))

    def preprocess_osc(self, osc_msg):
        # sonic-pi uses 'note' instead of 'freq', so we have to translate
        osc_msg['note'] = freqtomidi(osc_msg['freq'])

        # Need to set frequency to 0 because this will cause the 'rate' to be
        # set to 0 for the startSound synth of the init node. This is important
        # because sonic-pi's synths use Out instead of ReplaceOut, so we don't
        # want the startSound synth to be adding anything to that bus.
        osc_msg['freq'] = 0

        # sonic-pi has a full ADSR, but if those values are not explicitly
        # passed, translate the 'sus' into the sustain or release
        # (depending on what the synthdef uses by default)
        if 'attack' not in osc_msg and \
                'decay' not in osc_msg and \
                'sustain' not in osc_msg and \
                'release' not in osc_msg:
            if self._arg_defaults['sustain'] > 0:
                osc_msg['sustain'] = osc_msg['sus']
            else:
                osc_msg['release'] = osc_msg['sus']
            # can't delete 'sus' yet because it's used by ServerManager
            # del osc_msg['sus']

class Container(dict):
    def __getattr__(self, attr):
        return self[attr]

pisynth = Container()

def LoadSonicPiSynths(sonic_pi_dir):
    synthinfo = os.path.join(sonic_pi_dir, 'app/server/sonicpi/lib/sonicpi/synths/synthinfo')
    datastr = check_output(["ruby", "generate.rb", synthinfo])
    data = json.loads(datastr)
    for key, synthdata in data.items():
        fullname = synthdata['prefix'] + synthdata['synth_name']
        filename = os.path.join(sonic_pi_dir, 'etc/synthdefs/compiled/', fullname + '.scsyndef')
        synth = SonicPiSynthDef(fullname, filename, synthdata)
        synth.add()
        pisynth[key] = synth
