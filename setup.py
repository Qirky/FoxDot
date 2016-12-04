#!/usr/bin/env python

from distutils.core import setup   

setup(name='FoxDot',
      version='0.2.0',
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
      package_data = {'FoxDot': ['snd/*/*/*.*', 'osc/OSCFunc.scd'],
                      'FoxDot.lib.SCLang': ['scsyndef/*.scd'],
                      'FoxDot.lib.Workspace': ['img/*']})
