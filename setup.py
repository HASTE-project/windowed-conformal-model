#!/usr/bin/env python

from distutils.core import setup

setup(name='haste_windowed_conformal',
      packages=['haste.windowed_conformal_model',
                'haste.windowed_conformal_model.offline_data'],
      install_requires=[
          'pymongo', 'numpy', 'sklearn',
          'pandas', 'pygam',  # For time_series_features
      ],
      )
