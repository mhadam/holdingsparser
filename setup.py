from setuptools import setup

setup(name='holdingsparser',
      version='0.1.0',
      packages=['holdingsparser'],
      entry_points={
          'console_scripts': [
              'holdingsparser = holdingsparser.__main__:main'
          ]
      },
      )