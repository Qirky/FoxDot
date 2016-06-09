#!/usr/bin/env python

from distutils.core import setup

setup(name='FoxDot',
      version='0.1.2',
      description='Live Coding with SuperCollider',
      author='Ryan Kirkbride',
      author_email='sc10rpk@leeds.ac.uk',
      url='http://foxdot.org/',
      packages=['FoxDot',
                'FoxDot.Code',
                'FoxDot.Custom',
                'FoxDot.Interface',
                'FoxDot.Patterns',
                'FoxDot.SuperCollider'],
      py_modules=['main'],      
      package_data={'FoxDot':['Settings/*',
                              'SuperCollider/*',
                              'Samples/*',
                              'Samples/foxdot/*',
                              'Interface/*.ttf',
                              'foxdot.scd'] } )
