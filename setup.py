#!/usr/bin/env python

from setuptools import setup

setup(name='haste-windowed-conformal',
      packages=['haste.windowed_conformal_model',
                'haste.windowed_conformal_model.offline_data'],
      namespace_packages=['haste'],
      install_requires=[
          'pymongo', 'numpy', 'sklearn',
          'pandas', 'pygam',  # For time_series_features
      ]
      )
