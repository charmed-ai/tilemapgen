#!/usr/bin/env python

from distutils.core import setup

setup(name='tilemapgen',
      version='0.0.1',
      description='Generate isometric tilemaps from text prompts',
      author='Jeremy Tryba',
      author_email='jeremy@charmed.ai',
      url='https://github.com/charmed-ai/tilemap-generator/',
      packages=['tilemapgen'],
      package_dir={'': 'src'},
      py_modules=['tilemapgen'],
      install_requires=[
          'torch==2.0.1',
          'torchvision==0.15.2',
          'transformers',
          'diffusers',
          'pyrallis',
          'pytorch3d'
      ],
      scripts=['scripts/tilemapgen'],
     )