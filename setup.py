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
          'torch',
          'torchvision',
          'transformers',
          'diffusers',
          'pyrallis',
      ],
      scripts=['scripts/tilemapgen'],
     )