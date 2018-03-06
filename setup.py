#!/usr/bin/env python

from distutils.core import setup

setup(name='haste_windowed_conformal',
      packages=['haste.windowed_conformal_model'],
      install_requires=[
          'pymongo', 'numpy', 'sklearn'
      ],
      )
