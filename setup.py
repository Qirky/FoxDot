#!/usr/bin/env python

from distutils.core import setup   

setup(name='FoxDot',
      version='0.3.1',
      description='Live Coding with SuperCollider',
      author='Ryan Kirkbride',
      author_email='sc10rpk@leeds.ac.uk',
      url='http://foxdot.org/',
      packages=['FoxDot',
                'FoxDot.lib',
                'FoxDot.lib.Code',
                'FoxDot.lib.Custom',
                'FoxDot.lib.Workspace',
                'FoxDot.lib.Patterns',
                'FoxDot.lib.SCLang',
                'FoxDot.lib.Settings'],
      package_data = {'FoxDot': ['snd/*/*/*.*',
                                 'osc/*.scd',
                                 'osc/sceffects/*.scd',
                                 'osc/scsyndef/*.scd'],
                      'FoxDot.lib.Workspace': ['img/*'],
                      'FoxDot.lib.Settings' : ['conf.txt']})
