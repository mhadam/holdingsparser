import os
from setuptools import setup

with open('requirements.txt') as f:
	required = f.read().splitlines()

setup(name='holdingsparser',
      version='0.1.0',
      install_requires=required,
      packages=['holdingsparser'],
      entry_points={
          'console_scripts': [
              'holdingsparser = holdingsparser.__main__:main'
          ]
      },
      )