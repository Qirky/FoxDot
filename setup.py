#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

with open("README.md", "r") as f:
    long_description=f.read()

setup(name='FoxDot',
      version='0.6.5',
      description='Live coding music with SuperCollider',
      author='Ryan Kirkbride',
      author_email='ryan@foxdot.org',
      url='http://foxdot.org/',
      packages=['FoxDot',
                'FoxDot.lib',
                'FoxDot.lib.Code',
                'FoxDot.lib.Custom',
                'FoxDot.lib.Extensions',
                'FoxDot.lib.Workspace',
                'FoxDot.lib.Patterns',
                'FoxDot.lib.SCLang',
                'FoxDot.lib.Settings',
                'FoxDot.lib.Utils'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      entry_points={'gui_scripts' : ['FoxDot = FoxDot.__init__:main']},
      package_data = {'FoxDot': ['snd/*/*/*.*',
                                 'snd/_loop_/foxdot.wav',
                                 'snd/_loop_/drums130.wav',
                                 'snd/_loop_/dirty120.wav',
                                 'snd/_loop_/afro105.wav',
                                 'snd/_loop_/break170.wav',
                                 'snd/_loop_/cowbells110.wav',
                                 'snd/_loop_/robot110.wav',
                                 'snd/_loop_/techno130.wav',
                                 'osc/*.scd',
                                 'osc/sceffects/*.scd',
                                 'osc/scsyndef/*.scd',
                                 'demo/*.py',
                                 'lib/Extensions/*.json',
                                 ],
                      'FoxDot.lib.Workspace': ['img/*', 'tmp/*'],
                      'FoxDot.lib.Settings' : ['conf.txt']})
