from __future__ import print_function

import os

import json
from subprocess import check_output

from ..Midi import freqtomidi
from ..SCLang import CompiledSynthDef
from ..Settings import SYNTHDEF_DIR


try:
    from urllib import urlretrieve
except ImportError:
    # Python 3
    from urllib.request import urlretrieve


HERE = os.path.dirname(__file__)
SONIC_PI_FILE = os.path.join(HERE, 'sonicpi.json')
RUBY_SCRIPT = os.path.join(HERE, "generate.rb")


class Container(dict):
    """ Simple dict that allows access to keys via properties """
    def __getattr__(self, attr):
        return self[attr]

pisynth = Container()


class SonicPiSynthDef(CompiledSynthDef):
    bus_name = 'out_bus'

    def __init__(self, name, filename, synthdata):
        super(SonicPiSynthDef, self).__init__(name, filename)
        # These synths are all really loud for some reason
        self.balance = 0.2
        self._arg_defaults = synthdata['arg_defaults']
        for key in self._arg_defaults:
            if not hasattr(self, key):
                setattr(self, key, self.new_attr_instance(key))

    def preprocess_osc(self, osc_msg):
        super(SonicPiSynthDef, self).preprocess_osc(osc_msg)

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


def _load_synths(data, create_filename):
    for key, synthdata in data.items():
        # Don't handle FX or non-user facing synths (e.g. mixer) yet
        if not synthdata['is_synth'] or not synthdata['user_facing']:
            continue
        fullname = synthdata['prefix'] + synthdata['synth_name']
        filename = create_filename(fullname)
        synth = SonicPiSynthDef(fullname, filename, synthdata)
        synth.add()
        pisynth[key] = synth


def LoadSonicPiSynthsDev(sonic_pi_dir):
    """ Load the sonic pi synths from a live sonic-pi repo """
    synthinfo = os.path.join(sonic_pi_dir,
                             'app/server/sonicpi/lib/sonicpi/synths/synthinfo')
    datastr = check_output(["ruby", RUBY_SCRIPT, synthinfo])
    data = json.loads(datastr)
    _load_synths(
        data,
        lambda fn: os.path.join(sonic_pi_dir,
                                'etc/synthdefs/compiled/', fn + '.scsyndef')
    )


def LoadSonicPiSynths(metadata_file=SONIC_PI_FILE):
    """ Load sonic-pi synths from json metadata, downloading compiled synths if needed """
    with open(metadata_file, 'r') as ifile:
        data = json.load(ifile)
    ref = data.pop('__ref__')
    def create_filename(fullname):
        filename = os.path.join(SYNTHDEF_DIR, fullname + '.scsyndef')
        if not os.path.exists(filename):
            url = "https://github.com/samaaron/sonic-pi/raw/%s/etc/synthdefs/compiled/%s.scsyndef" % (ref, fullname)
            print("Downloading", url)
            urlretrieve(url, filename)
        return filename
    _load_synths(data, create_filename)


def GenerateSonicPiData(sonic_pi_dir):
    """ Generate the sonic-pi json metadata from a sonic-pi source repo """
    synthinfo = os.path.join(sonic_pi_dir,
                             'app/server/sonicpi/lib/sonicpi/synths/synthinfo')
    datastr = check_output(["ruby", RUBY_SCRIPT, synthinfo])
    ref = check_output(["git", "rev-parse", "HEAD"], cwd=sonic_pi_dir).strip()
    data = json.loads(datastr)
    data['__ref__'] = ref
    with open(SONIC_PI_FILE, 'w') as ofile:
        json.dump(data, ofile, separators=(',', ':'))
